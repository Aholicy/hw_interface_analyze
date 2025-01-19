import os
import re
from clang.cindex import Config, Index, CursorKind

# 设置 Clang 库路径
libclang_path = "/usr/lib/llvm-14/lib/libclang.so"
if not os.path.exists(libclang_path):
    raise RuntimeError(f"libclang not found at {libclang_path}")
Config.set_library_file(libclang_path)

def traverse_ast(cursor, output_file, level=0):
    """递归遍历 AST 并输出每个节点的详细信息"""
    indent = " " * (level * 2)  # 用空格进行缩进
    cursor_info = f"{indent}Cursor Kind: {cursor.kind} | Spelling: {cursor.spelling} | Location: {cursor.location.file}:{cursor.location.line}:{cursor.location.column}"
    output_file.write(cursor_info + "\n")

    # 遍历所有子节点
    for child in cursor.get_children():
        traverse_ast(child, output_file, level + 1)

def is_in_source_file(cursor, source_code_file):
    """检查 AST 节点是否属于源文件"""
    location = cursor.location
    if not location.file:  # 没有文件路径的节点直接排除
        return False
    return os.path.samefile(location.file.name, source_code_file)




def parse_file(file_path):
    """解析 C++ 文件并返回 AST 根节点"""
    index = Index.create()
    print(f"Parsing file: {file_path}")
    # 添加 include 路径作为参数

    # tu = index.parse(file_path, args=['-std=c++17', '-stdlib=libc++', f'-I{include_path}'])
    standard_lib_path = "/usr/lib/llvm-14/lib/clang/14.0.0"  
    # args = ['-std=c++17', '-stdlib=libc++', f'-I{standard_lib_path}']
    # args = ['-std=c++17', '-stdlib=libc++', f'-I{standard_lib_path}', '@include_dirs.txt']
    # args.extend([f'-I{path}' for path in include_dirs])
    # 输出参数，确认传递了正确的值
    # 基础参数，包括响应文件
    args = [
        '-std=c++17',
        '-stdlib=libc++',
        f'-I{standard_lib_path}',
        '-I/usr/include/c++/12',
        '-I/usr/include/x86_64-linux-gnu/c++/12/',
        # '-L/usr/lib/gcc/x86_64-linux-gnu/7',
        '-Dsize_t=unsigned long',  # 添加占位符定义
        '-ferror-limit=1000', # 允许错误限制
    ]
    # args = [
    #     '-std=c++17',                             # 使用 C++17 标准
    #     '-stdlib=libstdc++',                      # 指定使用 libstdc++
    #     f'-I/usr/include/c++/12',                 # libstdc++ 的主头文件路径
    #     # f'-I/usr/include/x86_64-linux-gnu/c++/12', # 多架构支持路径
    #     f'-L/usr/lib/gcc/x86_64-linux-gnu/12',    # GCC 标准库链接路径
    #     '-I/usr/lib/llvm-14/lib/clang/14.0.0/include', # Clang 自带头文件路径
    #     '-I/usr/include',                         # 系统默认头文件路径
    #     '-I/usr/local/include',                   # 本地用户安装路径
    #     '-include/usr/lib/llvm-14/lib/clang/14.0.0/include/stddef.h', # 强制包含 stddef.h
    # ]
    # args = [
    #     '-std=c++11',                             
    #     '-stdlib=libc++',                      
    #     '-std=c++11', '-stdlib=libc++',
    #     '-I/usr/lib/llvm-14/lib/clang/14.0.0',  
    #     '-I/usr/include/c++/11',
    #     '-I/usr/include/x86_64-linux-gnu/c++/11/',
    #     '-I/usr/local/include/grpc++/',
    #     '-include/usr/lib/llvm-14/lib/clang/14.0.0/include/stddef.h',
    # ]
    # 确保路径正确，直接扩展包含目录参数
    include_dirs_file = 'include_dirs.txt'  # 确保此文件路径正确

    if os.path.exists(include_dirs_file):  # 确保响应文件存在
        with open(include_dirs_file, 'r') as f:
            include_dirs = f.readlines()
            for line in include_dirs:
                # print(f"Include dir: {line.strip()}")
                args.append(line.strip())
    else:
        print(f"Warning: {include_dirs_file} not found.")
    tu = index.parse(file_path, args=args)
    if not tu:
        raise Exception(f"Failed to parse file: {file_path}")
    if tu.diagnostics:
        for diag in tu.diagnostics:
            print(f"Diagnostic: {diag.spelling} in {diag.location.file}:{diag.location.line}:{diag.location.column}")
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


def extract_blocks(cursor, source_code_file, namespace_stack=None):
    """递归提取所有代码块"""
    if namespace_stack is None:
        namespace_stack = []

    blocks = []
    for child in cursor.get_children():
        # 筛选需要的代码块类型，并且确保它属于源文件
        if child.kind in [
            CursorKind.CXX_TRY_STMT,
            CursorKind.CXX_CATCH_STMT,
            CursorKind.FUNCTION_DECL,
            CursorKind.CXX_METHOD,
        ] and is_in_source_file(child, source_code_file):
            blocks.append((get_block_type(child), child, namespace_stack.copy()))

        elif child.kind in [
            CursorKind.IF_STMT,
            CursorKind.FOR_STMT,
            CursorKind.WHILE_STMT,
            CursorKind.DO_STMT,
            CursorKind.SWITCH_STMT,
        ]and is_in_source_file(child, source_code_file):
            blocks.append((get_block_type(child), child, namespace_stack.copy()))
        
        # 递归处理子节点
        blocks.extend(extract_blocks(child, source_code_file, namespace_stack))
    
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
        r'TAG_LOG[DIWEF]',
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
    blocks = extract_blocks(cursor, file_path)  # 传递 file_path 作为 source_code_file
    with open(output_analysis_file, 'w', encoding='utf-8') as analysis_output:
        for block_type, block, namespace_stack in blocks:
            block_code = extract_block_source_code(block, source_code)
            if not block_code.strip():
                continue
            is_logged = contains_logging_statement(block_code)
            analysis_output.write(f"代码块类型: {block_type}\n")
            analysis_output.write(f"位置: {block.location.line}:{block.location.column}\n")
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
    source_dir = "../ability_ability_runtime/interfaces/inner_api"
    ast_output_dir = "ast_output"
    analysis_output_dir = "analysis_output"

    analyze_directory(source_dir, ast_output_dir, analysis_output_dir)
    print(f"Analysis completed. AST and block analysis saved in {ast_output_dir} and {analysis_output_dir}")


if __name__ == "__main__":
    main()
