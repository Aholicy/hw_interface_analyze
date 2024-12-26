import clang.cindex
import os
import re
import json
import shlex

# 初始化libclang
clang.cindex.Config.set_library_file("/usr/lib/llvm-14/lib/libclang.so")  # 修改为你的libclang路径

# 读取文件中的代码片段
def get_source_code_from_extent(extent):
    with open(extent.start.file.name, 'r') as f:
        lines = f.readlines()

    # 获取片段的起始和结束位置
    start_line = extent.start.line
    start_col = extent.start.column
    end_line = extent.end.line
    end_col = extent.end.column

    # 提取代码片段
    if start_line == end_line:
        return lines[start_line - 1][start_col - 1:end_col - 1]
    else:
        body_lines = [lines[start_line - 1][start_col - 1:]]
        body_lines.extend(lines[start_line:end_line - 1])
        body_lines.append(lines[end_line - 1][:end_col - 1])
        return ''.join(body_lines)

# 递归遍历AST
def visit_children(source, node, filename, function_dependencies):
    for child in node.get_children():
        if str(child.location.file) != filename:
            continue

        # 处理函数声明
        if child.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            function_name = str(child.spelling)
            source['function'][function_name] = get_source_code_from_extent(child.extent)
            function_dependencies[function_name] = set()  # 初始化该函数的依赖关系

        # 处理函数调用
        elif child.kind == clang.cindex.CursorKind.CALL_EXPR:
            called_function = str(child.spelling)  # 获取被调用函数的名称
            if called_function:
                caller_function = str(node.spelling)
                if caller_function and caller_function in function_dependencies:
                    function_dependencies[caller_function].add(called_function)

        # 处理结构体声明
        elif child.kind == clang.cindex.CursorKind.STRUCT_DECL:
            source['head']['struct'][str(child.spelling)] = get_source_code_from_extent(child.extent)

        # 处理全局变量声明
        elif child.kind == clang.cindex.CursorKind.VAR_DECL:
            if child.linkage == clang.cindex.LinkageKind.EXTERNAL:  # 过滤出全局变量
                source['head']['global_variable'][str(child.spelling)] = get_source_code_from_extent(child.extent)

        # 处理typedef声明
        elif child.kind == clang.cindex.CursorKind.TYPEDEF_DECL:
            source['head']['typedef'][str(child.spelling)] = get_source_code_from_extent(child.extent)

        elif child.kind == clang.cindex.CursorKind.ENUM_DECL:
            source['head']['enum'][str(child.spelling)] = get_source_code_from_extent(child.extent)

        # 递归处理子节点
        visit_children(source, child, filename, function_dependencies)

# 分析源代码文件
def analyze_precomiled_file(source, filename):
    # 创建索引
    index = clang.cindex.Index.create()

    # 解析源文件
    translation_unit = index.parse(filename)

    # 初始化函数依赖关系字典
    function_dependencies = {}

    # 遍历抽象语法树 (AST)
    visit_children(source, translation_unit.cursor, filename, function_dependencies)

    return function_dependencies

def analyze_file_dependency(filename):
    pass

def filter_source_file(filename, new_filename):
    with open(new_filename, 'r') as f:
        content = f.read()
    content = [line for line in content.splitlines() if line.strip()]
    line_number = []
    pattern = r'#\s+\d+\s+\"([^ ]+)\"'
    for i, line in enumerate(content):
        res = re.findall(pattern, line)
        if len(res) > 0:
            line_number.append(i)
    
    i = 0
    source_file = ''
    while i < len(line_number):
        res = re.findall(pattern, content[line_number[i]])
        if len(res) > 0 and res[0] == filename:
            if i == len(line_number) - 1:
                source_file += '\n'.join(content[line_number[i]+1:])
            else:
                source_file += '\n'.join(content[line_number[i]+1:line_number[i+1]])
        i += 1

    with open(new_filename, 'w') as f:
        f.write(source_file)

    os.system(f'clang-format -style=google -i {shlex.quote(new_filename)}')

def analyze(filename, CFLAGS = '-E -O2 -Wall -DALLOC_TESTING', INCLUDE = ''):
    name, ext = os.path.splitext(filename)
    new_filename = './Output/' + os.path.basename(name) + '.tmp' + ext

    # 确保输出目录存在
    if not os.path.exists('./Output'):
        os.makedirs('./Output')

    # 更新为clang++并添加标准库路径
    compile_command = [
        'clang++', CFLAGS, INCLUDE,
        '-std=c++11', '-stdlib=libc++',
        '-I/usr/lib/llvm-14/lib/clang/14.0.0',  # 示例路径，可能需要根据你的环境调整
        '-I/usr/include/c++/11',
        '-I/usr/include/x86_64-linux-gnu/c++/11/',
        filename, '-o', new_filename,
        '-x','c++'
    ]
    result = os.system(' '.join(compile_command))
    
    if result != 0:
        print(f"Error compiling {filename}")
        return None, None  # 返回None值，避免解包错误

    filter_source_file(filename, new_filename)
    
    source = {}
    source['head'] = {}
    source['head']['struct'] = {}
    source['head']['global_variable'] = {}
    source['head']['typedef'] = {}
    source['head']['enum'] = {}
    source['function'] = {}

    # 分析预处理后的文件并获取函数依赖关系
    function_dependencies = analyze_precomiled_file(source, new_filename)

    return source, function_dependencies

def get_include_paths(base_dir):
    include_paths = []
    header_files = []  # 用来保存所有头文件的路径

    for root, dirs, files in os.walk(base_dir):
        if 'include' in dirs:
            include_paths.append(f'-I{os.path.join(root, "include")}')
        # Add all subdirectories for header files
        for file in files:
            if file.endswith(".h"):
                header_files.append(os.path.join(root, file))  # 保存头文件路径
                include_paths.append(f'-I{root}')
    
    # 输出所有解析出的头文件名到一个文件
    with open('./Output/header_files.txt', 'w') as f:
        for header_file in header_files:
            f.write(header_file + '\n')
    
    return include_paths

def analyze_directory(directory,include_dic):
    include_paths = get_include_paths(include_dic)
    include_str = ' '.join(include_paths)
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".c") or file.endswith(".h"):
                filename = os.path.join(root, file)
                print(f"Analyzing {filename}")
                source, function_dependencies = analyze(filename, INCLUDE=include_str)
                
                if source and function_dependencies:
                    # 输出到对应的文件
                    output_file = f"./Output/{os.path.basename(filename)}_dependencies.json"
                    with open(output_file, 'w') as f:
                        json.dump({
                            "source": source,
                            "function_dependencies": function_dependencies
                        }, f, indent=4)
                    print(f"Results written to {output_file}")


def main():
    include_dic="ability_ability_runtime"
    ana_dic="ability_ability_runtime/interfaces/inner_api/ability_manager"
    analyze_directory(ana_dic,include_dic)

if __name__ == "__main__":
    main()
