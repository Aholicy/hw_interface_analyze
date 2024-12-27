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

# 递归遍历AST，收集跨文件依赖
def visit_children(source, node, filename, function_dependencies, file_dependencies, debug_info):
    for child in node.get_children():
        # Debug信息：输出每个AST节点的类型和位置
        debug_info.append(f"Visiting Node: {child.kind}, {child.spelling}, Location: {child.location}")

        if str(child.location.file) != filename:
            continue

        # 处理命名空间声明
        if child.kind == clang.cindex.CursorKind.NAMESPACE:
            namespace_name = str(child.spelling)
            source['head']['namespace'] = namespace_name  # 保存namespace信息
            debug_info.append(f"Namespace found: {namespace_name}")

        # 处理枚举声明
        elif child.kind == clang.cindex.CursorKind.ENUM_DECL:
            enum_name = str(child.spelling)
            source['head']['enum'][enum_name] = get_source_code_from_extent(child.extent)
            debug_info.append(f"Enum found: {enum_name}")

        # 处理类声明
        elif child.kind == clang.cindex.CursorKind.CLASS_DECL:
            class_name = str(child.spelling)
            source['head']['class'] = class_name  # 保存class信息
            debug_info.append(f"Class found: {class_name}")

        # 处理函数声明
        elif child.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            function_name = str(child.spelling)
            source['function'][function_name] = get_source_code_from_extent(child.extent)
            function_dependencies[function_name] = set()  # 初始化该函数的依赖关系
            debug_info.append(f"Function found: {function_name}")

        # 处理函数调用
        elif child.kind == clang.cindex.CursorKind.CALL_EXPR:
            called_function = str(child.spelling)  # 获取被调用函数的名称
            if called_function:
                caller_function = str(node.spelling)
                if caller_function and caller_function in function_dependencies:
                    function_dependencies[caller_function].add(called_function)

                    # 记录跨文件调用
                    called_file = str(child.location.file)
                    if called_file != filename:
                        if called_file not in file_dependencies:
                            file_dependencies[called_file] = {}
                        if called_function not in file_dependencies[called_file]:
                            file_dependencies[called_file][called_function] = []
                        file_dependencies[called_file][called_function].append(filename)

                    # 记录函数调用调试信息
                    debug_info.append(f"Function '{caller_function}' calls '{called_function}' in file '{called_file}'")

        # 处理结构体声明
        elif child.kind == clang.cindex.CursorKind.STRUCT_DECL:
            struct_name = str(child.spelling)
            source['head']['struct'][struct_name] = get_source_code_from_extent(child.extent)
            debug_info.append(f"Struct found: {struct_name}")

        # 处理全局变量声明
        elif child.kind == clang.cindex.CursorKind.VAR_DECL:
            if child.linkage == clang.cindex.LinkageKind.EXTERNAL:  # 过滤出全局变量
                if child.spelling != "OHOS":  # 防止错误识别为全局变量
                    source['head']['global_variable'][str(child.spelling)] = get_source_code_from_extent(child.extent)
                    debug_info.append(f"Global Variable found: {child.spelling}")

        # 处理typedef声明
        elif child.kind == clang.cindex.CursorKind.TYPEDEF_DECL:
            typedef_name = str(child.spelling)
            source['head']['typedef'][typedef_name] = get_source_code_from_extent(child.extent)
            debug_info.append(f"Typedef found: {typedef_name}")

        # 递归处理子节点
        visit_children(source, child, filename, function_dependencies, file_dependencies, debug_info)

# 分析预处理后的文件
def analyze_precompiled_file(source, filename, debug_info):
    # 创建索引
    index = clang.cindex.Index.create()

    # 解析源文件
    translation_unit = index.parse(filename)
    
    # Debug信息：输出是否成功解析文件
    debug_info.append(f"Parsed file: {filename}, AST root: {translation_unit.cursor.kind}")
    
    # 初始化函数依赖关系字典
    function_dependencies = {}
    file_dependencies = {}  # 用来记录跨文件依赖

    # 遍历抽象语法树 (AST)
    visit_children(source, translation_unit.cursor, filename, function_dependencies, file_dependencies, debug_info)

    return function_dependencies, file_dependencies

# 过滤和格式化源文件
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

# 分析源代码文件和依赖关系
def analyze(filename, CFLAGS = '-E', INCLUDE = '', debug_info = []):
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
        return {}, {}, {}  # 返回空字典，避免解包错误

    filter_source_file(filename, new_filename)
    
    source = {}
    source['head'] = {}
    source['head']['struct'] = {}
    source['head']['global_variable'] = {}
    source['head']['typedef'] = {}
    source['head']['enum'] = {}
    source['head']['namespace'] = {}  # 新增字段，存储namespace信息
    source['function'] = {}

    # 分析预处理后的文件并获取函数依赖关系
    function_dependencies, file_dependencies = analyze_precompiled_file(source, new_filename, debug_info)

    # 如果没有找到依赖关系，确保返回空字典
    if not function_dependencies:
        function_dependencies = {}
    if not file_dependencies:
        file_dependencies = {}

    return source, function_dependencies, file_dependencies

# 获取包含路径
def get_include_paths(include_dic):
    include_paths = []
    header_files = []  # 用来保存所有头文件的路径
    for base_dir in include_dic:
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

# 分析目录下所有文件
def analyze_directory(directory, include_dic):
    include_paths = get_include_paths(include_dic)
    include_str = ' '.join(include_paths)
    
    debug_info = []  # 用于保存调试信息
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".c") or file.endswith(".h"):
                filename = os.path.join(root, file)
                print(f"Analyzing {filename}")  # 输出正在分析的文件路径
                source, function_dependencies, file_dependencies = analyze(filename, INCLUDE=include_str, debug_info=debug_info)
                
                if source and function_dependencies:
                    output_file = f"./Output/{os.path.basename(filename)}_dependencies.json"
                    try:
                        with open(output_file, 'w') as f:
                            json.dump({
                                "source": source,
                                "function_dependencies": function_dependencies,
                                "file_dependencies": file_dependencies  # 添加文件间依赖信息
                            }, f, indent=4)
                        print(f"Results written to {output_file}")
                    except Exception as e:
                        print(f"Error writing to {output_file}: {e}")
    
    # 将调试信息保存到txt文件
    with open('./Output/dependencies_debug.txt', 'w') as debug_file:
        for line in debug_info:
            debug_file.write(line + '\n')

def main():
    include_dic = ["ability_ability_runtime", "ability_ability_base"]
    ana_dic = "ability_ability_runtime/interfaces/inner_api/ability_manager"
    analyze_directory(ana_dic, include_dic)

if __name__ == "__main__":
    main()
