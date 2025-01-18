import os
import re
from clang.cindex import Config, Index, CursorKind

# 设置 Clang 库路径
libclang_path = "/usr/lib/llvm-14/lib/libclang.so"
if not os.path.exists(libclang_path):
    raise RuntimeError(f"libclang not found at {libclang_path}")
Config.set_library_file(libclang_path)

# 设置 include 文件夹路径
# include_path = "/home/user/yzb/hw_interface_analyze/interface_test/test_c/ability_ability_runtime/interfaces/inner_api/ability_manager/include"
# if not os.path.exists(include_path):
#     raise RuntimeError(f"Include path not found: {include_path}")
source_root = "../ability_ability_runtime/interfaces/inner_api/ability_manager"
include_dirs = []
# for root, dirs, _ in os.walk(source_root):
#     for dir_name in dirs:
#         if dir_name == "include":
#             include_dirs.append(os.path.join(root, dir_name))
# if not include_dirs:
#     raise RuntimeError("No include directories found in the source root.")     
# 查找所有 include 目录及其子目录
for root, dirs, _ in os.walk(source_root):
    for dir_name in dirs:
        if dir_name == "include":
            # 遍历该 include 文件夹及其所有子文件夹
            include_path = os.path.join(root, dir_name)
            for root_dir, subdirs, _ in os.walk(include_path):
                include_dirs.append(root_dir)  # 将所有子文件夹路径添加到 include_dirs 列表

if not include_dirs:
    raise RuntimeError("No include directories found in the source root.")   
# 将所有的 include 目录路径输出到文件
def output_include_dirs(file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for dir_path in include_dirs:
            f.write(dir_path + "\n")
    print(f"All include directories have been saved to {file_path}")

# 调用函数保存 include 目录到文件
output_include_dirs("include_dirs.txt")

def traverse_ast(cursor, output_file, level=0):
    """递归遍历 AST 并输出每个节点的详细信息"""
    indent = " " * (level * 2)  # 用空格进行缩进
    cursor_info = f"{indent}Cursor Kind: {cursor.kind} | Spelling: {cursor.spelling} | Location: {cursor.location.line}:{cursor.location.column}"
    output_file.write(cursor_info + "\n")

    # 遍历所有子节点
    for child in cursor.get_children():
        traverse_ast(child, output_file, level + 1)

def is_in_source_file(cursor, source_code):
    """检查 AST 节点的 spelling 是否在源文件中"""
    spelling = cursor.spelling.strip()
    if not spelling:
        return False

    # 检查 spelling 是否出现在源文件中
    for line in source_code:
        if spelling in line:
            return True
    return False


def parse_file(file_path):
    """解析 C++ 文件并返回 AST 根节点"""
    index = Index.create()
    print(f"Parsing file: {file_path}")
    # 添加 include 路径作为参数

    # tu = index.parse(file_path, args=['-std=c++17', '-stdlib=libc++', f'-I{include_path}'])
    standard_lib_path = "/usr/lib/llvm-14/lib/clang/14.0.0"  
    args = ['-std=c++17', '-stdlib=libc++', f'-I{standard_lib_path}']
    args.extend([f'-I{path}' for path in include_dirs])
    tu = index.parse(file_path, args=args)
    if not tu:
        raise Exception(f"Failed to parse file: {file_path}")
    if tu.diagnostics:
        for diag in tu.diagnostics:
            print(f"Diagnostic: {diag.spelling}")
    print(f"File parsed successfully: {file_path}")
    return tu.cursor


def get_block_type(cursor):
    """根据 CursorKind 确定代码块类型"""
    if cursor.kind == CursorKind.FUNCTION_DECL:
        return "Function Declaration"
    elif cursor.kind == CursorKind.CXX_METHOD:
        return "Method Declaration"
    elif cursor.kind == CursorKind.CLASS_DECL:
        return "Class Declaration"
    elif cursor.kind == CursorKind.ENUM_DECL:
        return "Enum Declaration"
    elif cursor.kind == CursorKind.IF_STMT:
        return "Conditional Block (if)"
    elif cursor.kind in [CursorKind.FOR_STMT, CursorKind.WHILE_STMT, CursorKind.DO_STMT]:
        return f"Loop Block ({cursor.kind.name.lower().replace('_stmt', '')})"
    elif cursor.kind == CursorKind.SWITCH_STMT:
        return "Switch Block"
    elif cursor.kind in [CursorKind.CXX_TRY_STMT, CursorKind.CXX_CATCH_STMT]:
        return "Exception Handling Block"
    elif cursor.kind == CursorKind.NAMESPACE:
        return "Namespace Declaration"
    return "Other Block"


def get_complete_block(cursor):
    """获取完整的代码块范围，包括所有相关的子块"""
    start = cursor.extent.start
    end = cursor.extent.end

    if cursor.kind in [CursorKind.FUNCTION_DECL, CursorKind.CXX_METHOD]:
        for child in cursor.get_children():
            if child.kind == CursorKind.COMPOUND_STMT:  # 方法体的实际代码块
                end = child.extent.end
                break

    if cursor.kind == CursorKind.IF_STMT:
        for child in cursor.get_children():
            if child.kind == CursorKind.COMPOUND_STMT:
                child_end = child.extent.end
                if child_end.line > end.line or (
                    child_end.line == end.line and child_end.column > end.column
                ):
                    end = child_end

    elif cursor.kind == CursorKind.CXX_TRY_STMT:
        for child in cursor.get_children():
            if child.kind == CursorKind.CXX_CATCH_STMT:
                child_end = child.extent.end
                if child_end.line > end.line or (
                    child_end.line == end.line and child_end.column > end.column
                ):
                    end = child_end

    return start, end


def extract_block_source_code(block, source_code):
    """提取完整的代码块源代码"""
    start, end = get_complete_block(block)
    start_line = max(0, start.line - 1)
    end_line = min(len(source_code), end.line)

    block_lines = source_code[start_line:end_line]
    return ''.join(block_lines)


def extract_blocks(cursor, source_code, namespace_stack=None):
    """递归提取所有代码块"""
    if namespace_stack is None:
        namespace_stack = []

    blocks = []
    for child in cursor.get_children():
        # if child.kind == CursorKind.NAMESPACE:
        #     # 进入新的命名空间
        #     namespace_stack.append(child.spelling)
        #     blocks.append((get_block_type(child), child, namespace_stack.copy()))
        #     blocks.extend(extract_blocks(child, source_code, namespace_stack))
        #     namespace_stack.pop()  # 离开当前命名空间
        if child.kind in [
            CursorKind.CXX_TRY_STMT,
            CursorKind.CXX_CATCH_STMT,
            CursorKind.FUNCTION_DECL,
            CursorKind.CXX_METHOD,
            # CursorKind.NAMESPACE,
        ] and is_in_source_file(child, source_code):
            blocks.append((get_block_type(child), child, namespace_stack.copy()))

        elif child.kind in [
            CursorKind.IF_STMT,
            CursorKind.FOR_STMT,
            CursorKind.WHILE_STMT,
            CursorKind.DO_STMT,
            CursorKind.SWITCH_STMT,
        ]:
            blocks.append((get_block_type(child), child, namespace_stack.copy()))
        
        blocks.extend(extract_blocks(child, source_code, namespace_stack))
    
    return blocks


def contains_logging_statement(code_block):
    """检查代码块是否包含日志语句"""
    logging_patterns = [
        r'\blog\s*\(',
        r'printf\s*\(',
        r'cout\s*<<',
        r'cerr\s*<<',
        r'clog\s*<<',
        r'fprintf\s*\(',
        r'LogMessage',
        r'Logger',
        r'LBSLOG[DIWE]',
    ]
    return any(re.search(pattern, code_block, re.IGNORECASE) for pattern in logging_patterns)


def analyze_cpp_file(file_path, output_ast_file, output_analysis_file):
    """解析单个 C++ 文件并分析代码块"""
    with open(file_path, 'r', encoding='utf-8') as file:
        source_code = file.readlines()

    cursor = parse_file(file_path)

    # AST 输出
    with open(output_ast_file, 'w', encoding='utf-8') as ast_output:
        traverse_ast(cursor, ast_output)

    # 代码块分析
    blocks = extract_blocks(cursor, source_code)
    with open(output_analysis_file, 'w', encoding='utf-8') as analysis_output:
        for block_type, block, namespace_stack in blocks:
            block_code = extract_block_source_code(block, source_code)
            if not block_code.strip():
                continue
            is_logged = contains_logging_statement(block_code)
            analysis_output.write(f"代码块类型: {block_type}\n")
            analysis_output.write(f"位置: {block.location.line}:{block.location.column}\n")
            # analysis_output.write(f"命名空间: {'::'.join(namespace_stack) if namespace_stack else 'N/A'}\n")
            analysis_output.write(f"Spell: {block.spelling}\n")
            analysis_output.write(f"包含日志: {'是' if is_logged else '否'}\n")
            analysis_output.write(f"代码:\n{block_code}\n")
            analysis_output.write("-" * 80 + "\n")


def analyze_directory(directory_path, output_ast_dir, output_analysis_dir):
    """分析目录中的所有 C++ 文件并保留文件夹层次结构"""
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".cpp"):
                # 源文件路径
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, directory_path)

                # 输出文件夹路径，保留原目录结构
                ast_output_subdir = os.path.join(output_ast_dir, relative_path)
                analysis_output_subdir = os.path.join(output_analysis_dir, relative_path)

                # 确保输出子目录存在
                os.makedirs(ast_output_subdir, exist_ok=True)
                os.makedirs(analysis_output_subdir, exist_ok=True)

                # 输出文件路径
                output_ast_file = os.path.join(ast_output_subdir, f"{file}_ast.txt")
                output_analysis_file = os.path.join(analysis_output_subdir, f"{file}_analysis.txt")

                # 解析和分析
                analyze_cpp_file(file_path, output_ast_file, output_analysis_file)

def main():
    """主函数"""
    source_dir = "../ability_ability_runtime/interfaces/inner_api/ability_manager/src"
    ast_output_dir = "ast_output"
    analysis_output_dir = "analysis_output"

    analyze_directory(source_dir, ast_output_dir, analysis_output_dir)
    print(f"Analysis completed. AST and block analysis saved in {ast_output_dir} and {analysis_output_dir}")


if __name__ == "__main__":
    main()
