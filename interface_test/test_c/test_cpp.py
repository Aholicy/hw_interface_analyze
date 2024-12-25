import os
import re
import json

def parse_cpp_file(file_path, module_name, parsed_data):
    """解析 CPP 文件，提取类、方法、头文件、函数调用等信息"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 提取头文件依赖
    includes = re.findall(r'#include\s+"([\w./]+)"', content)

    # 提取类和方法信息
    classes = []
    class_pattern = re.compile(r'class\s+(\w+)\s*(?::\s*public\s+\w+)?\s*\{([^}]*)\}', re.DOTALL)
    for class_match in class_pattern.finditer(content):
        class_name = class_match.group(1).strip()
        class_body = class_match.group(2).strip()

        methods = []
        method_pattern = re.compile(
            r'([a-zA-Z_][a-zA-Z0-9_ ]*\s+\*?\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*(const|override|= 0)?\s*{'
        )
        for method_match in method_pattern.finditer(class_body):
            return_type = method_match.group(1).strip()
            method_name = method_match.group(2).strip()
            parameters = method_match.group(3).strip()
            methods.append({
                'name': method_name,
                'return_type': return_type,
                'parameters': parameters
            })
        
        classes.append({
            'name': class_name,
            'methods': methods
        })

    # 提取函数调用
    function_calls = []
    call_pattern = re.compile(r'(\w+::\w+|\w+)\s*\(([^)]*)\)\s*;')
    for call_match in call_pattern.finditer(content):
        function_name = call_match.group(1).strip()
        arguments = call_match.group(2).strip()
        function_calls.append({
            'function': function_name,
            'arguments': arguments
        })

    # 生成该文件的依赖关系数据
    dependencies = {
        'module': module_name,
        'includes': includes,
        'classes': classes,
        'function_calls': function_calls
    }

    return dependencies

def analyze_cpp_files(src_folder, parsed_data):
    """分析 src 文件夹中的 CPP 文件，并保存解析结果"""
    result = {}
    for entry in os.scandir(src_folder):
        if entry.is_file() and entry.name.endswith('.cpp'):
            module_name = entry.name[:-4]
            result[module_name] = parse_cpp_file(entry.path, module_name, parsed_data)
    return result

def save_dependencies(output_file, dependencies):
    """保存依赖关系到新的文件"""
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(dependencies, file, indent=4, ensure_ascii=False)
    print(f"依赖关系已保存到 {output_file}")

def main():
    # 假设解析后的 JSON 数据已经加载
    with open('parsed_interfaces.json', 'r', encoding='utf-8') as file:
        parsed_data = json.load(file)

    src_folder = "ability_ability_runtime/interfaces/inner_api/ability_manager/src"  # 存放 CPP 文件的文件夹路径
    output_file = "cpp_dependencies.json"  # 输出文件路径

    # 解析 CPP 文件并获取依赖关系
    cpp_dependencies = analyze_cpp_files(src_folder, parsed_data)

    # 保存解析结果
    save_dependencies(output_file, cpp_dependencies)

if __name__ == "__main__":
    main()
