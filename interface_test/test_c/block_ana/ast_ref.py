import os
from clang.cindex import Config, Index, CursorKind

# 设置 Clang 库路径
libclang_path = "/usr/lib/llvm-14/lib/libclang.so"
if not os.path.exists(libclang_path):
    raise RuntimeError(f"libclang not found at {libclang_path}")
Config.set_library_file(libclang_path)

def is_in_source_file(cursor, source_code_file):
    """检查 AST 节点是否属于源文件，支持同名.h文件"""
    location = cursor.location
    if not location.file:  # 检查文件是否存在
        return False  # 没有文件路径的节点直接排除

    # 支持判断.h文件
    file_name = location.file.name
    if not os.path.samefile(file_name, source_code_file):
        # 如果不是 .cpp 文件，判断是否是同名 .h 文件
        source_code_base = os.path.splitext(source_code_file)[0].split("/")[-1]
        file_base = os.path.splitext(file_name)[0].split("/")[-1]
        print(f"source_code_base: {source_code_base}, file_base: {file_base}")
        return source_code_base == file_base

    return os.path.samefile(location.file.name, source_code_file)

def parse_file(file_path):
    """解析 C++ 文件并返回 AST 根节点"""
    index = Index.create()
    print(f"Parsing file: {file_path}")
    standard_lib_path = "/usr/lib/llvm-14/lib/clang/14.0.0"
    args = [
        '-std=c++17',
        '-stdlib=libc++',
        f'-I{standard_lib_path}',
        '-I/usr/include/c++/12',
        '-I/usr/include/x86_64-linux-gnu/c++/12/',
        '-Dsize_t=unsigned long',  # 添加占位符定义
        '-ferror-limit=1000',  # 允许错误限制
    ]

    include_dirs_file = 'include_dirs.txt'
    if os.path.exists(include_dirs_file):
        with open(include_dirs_file, 'r') as f:
            include_dirs = f.readlines()
            for line in include_dirs:
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

def process_node(cursor, output_file, file_path, depth=0):
    """递归处理 AST 节点"""
    indent = "  " * depth  # 生成当前层次的缩进

    if is_in_source_file(cursor, file_path):
        # 输出当前节点的信息
        output_file.write(f"{indent}- Node: {cursor.kind} | Name: {cursor.spelling} | Location: {cursor.location.file}:{cursor.location.line}:{cursor.location.column}\n")

        if cursor.kind in {CursorKind.TYPE_REF, CursorKind.NAMESPACE_REF, CursorKind.TEMPLATE_REF}:
            output_file.write(f"{indent}  - Node: {cursor.kind} | Name: {cursor.spelling} | Location: {cursor.location.file}:{cursor.location.line}:{cursor.location.column}\n")
            referenced = cursor.referenced
            if referenced:
                output_file.write(f"{indent}    -> Referenced: {referenced.kind} | Name: {referenced.spelling} | Location: {referenced.location.file}:{referenced.location.line}:{referenced.location.column}\n")

        # 判断函数调用（CALL_EXPR）
        if cursor.kind == CursorKind.CALL_EXPR:
                output_file.write(f"{indent}  -> Function Call: {cursor.spelling} | Location: {cursor.location.file}:{cursor.location.line}:{cursor.location.column}\n")
    # 递归处理子节点
    for child in cursor.get_children():
        process_node(child, output_file, file_path, depth + 1)

def analyze_cpp_file(file_path, output_analysis_file):
    """解析单个 C++ 文件并分析引用及父节点"""
    cursor = parse_file(file_path)
    with open(output_analysis_file, 'w', encoding='utf-8') as analysis_output:
        if cursor:
            process_node(cursor, analysis_output, file_path)

def analyze_directory(directory_path, output_analysis_dir):
    """分析目录中的所有 C++ 文件并保留文件夹层次结构"""
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".cpp"):
                # 源文件路径
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, directory_path)

                # 输出文件夹路径，保留原目录结构
                analysis_output_subdir = os.path.join(output_analysis_dir, relative_path)

                # 确保输出子目录存在
                os.makedirs(analysis_output_subdir, exist_ok=True)

                # 输出文件路径
                output_analysis_file = os.path.join(analysis_output_subdir, f"{file}_ref_ana.txt")

                # 解析和分析
                analyze_cpp_file(file_path, output_analysis_file)

def main():
    """主函数"""
    source_dir = "../ability_ability_runtime/interfaces/inner_api/ability_manager"  # 源文件夹
    analysis_output_dir = "ref_ana"  # 引用分析输出文件夹

    analyze_directory(source_dir, analysis_output_dir)
    print(f"Reference analysis completed. Analysis results saved in {analysis_output_dir}")

if __name__ == "__main__":
    main()
