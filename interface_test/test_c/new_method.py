import os
import re
import json

def parse_header_file(file_path, module_name):
    """解析头文件并提取接口和依赖关系"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    includes = re.findall(r'#include\s+"([\w./]+)"', content)
    enums = extract_enums(content)
    classes = extract_classes(content)

    return {
        'module': module_name,
        'includes': includes,
        'enums': enums,
        'classes': classes
    }

def extract_enums(content):
    """提取枚举类信息"""
    enums = []
    enum_pattern = re.compile(r'enum\s+class\s+(\w+)\s*\{([^}]*)\}', re.DOTALL)
    for match in enum_pattern.finditer(content):
        enum_name = match.group(1).strip()
        enum_values = [
            {
                'name': value.strip(),
                'ipc_id': (value.split('=')[1].strip() if '=' in value else None)
            }
            for value in re.sub(r'//.*', '', match.group(2)).split(',')
            if value.strip()
        ]
        enums.append({'name': enum_name, 'values': enum_values})
    return enums

def extract_classes(content):
    """提取类及其方法信息"""
    classes = {}
    class_pattern = re.compile(r'class\s+(\w+)\s*(?::\s*public\s+([\w:]+))?\s*\{([^}]*)\}', re.DOTALL)
    for match in class_pattern.finditer(content):
        class_name = match.group(1).strip()
        base_class = match.group(2).strip() if match.group(2) else None
        class_body = match.group(3).strip()

        method_pattern = re.compile(
            r'([a-zA-Z_][a-zA-Z0-9_:\* ]+\s+)([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*(const|override|= 0)?\s*;'
        )
        methods = []
        for m in method_pattern.finditer(class_body):
            raw_params = m.group(3).strip()
            param_list = parse_parameters(raw_params)  # 详细解析参数
            methods.append({
                'name': m.group(2).strip(),
                'return_type': m.group(1).strip(),
                'parameters': param_list,
                'is_const': m.group(4) is not None,
            })

        classes[class_name] = {
            'base_class': base_class,
            'methods': methods,
            'dependencies': {'inheritance': None, 'parameters': {}},  # 初始化 dependencies
        }
    return classes

def parse_parameters(parameters):
    """解析方法参数为类型和名称的列表"""
    param_list = []
    if not parameters.strip():
        return param_list
    params = parameters.split(',')
    for param in params:
        param = param.strip()
        if param:
            match = re.match(r'([a-zA-Z_][\w:<>*&\s]+)\s+([a-zA-Z_][\w]*)', param)
            if match:
                param_type = match.group(1).strip()
                param_name = match.group(2).strip()
                param_list.append({'type': param_type, 'name': param_name})
            else:
                param_list.append({'type': param, 'name': None})  # 处理无法解析的情况
    return param_list

def extract_parameter_types(parameter_string):
    """精确提取函数参数的类型"""
    if not parameter_string.strip():
        return []
    parameters = parameter_string.split(',')
    types = []
    for param in parameters:
        type_part = re.sub(r'[\w]+$', '', param).strip()  # 去掉变量名，仅保留类型
        type_part = type_part.replace('*', '').replace('&', '').strip()  # 处理指针和引用
        types.append(type_part)
    return types

def find_definitions(symbols, include_paths):
    """查找符号定义"""
    definitions = {}
    for include_path in include_paths:
        if not os.path.exists(include_path):
            continue
        with open(include_path, 'r', encoding='utf-8') as file:
            content = file.read()

        for symbol in symbols:
            if re.search(r'\b' + re.escape(symbol) + r'\b', content):
                definitions[symbol] = include_path
    return definitions

def analyze_dependencies(parsed_data, folder_path):
    """分析继承类和函数参数类型的依赖"""
    all_includes = set()

    for module, data in parsed_data.items():
     
        all_includes.update(data['includes'])
        include_paths = [os.path.join(folder_path, inc) for inc in data['includes']]
        
        for class_name, class_data in data['classes'].items():
            if 'dependencies' not in class_data:
                class_data['dependencies'] = {'inheritance': None, 'parameters': {}}

            # 继承类依赖
            base_class = class_data['base_class']
            if base_class:
                inheritance_definitions = find_definitions([base_class], include_paths)
                class_data['dependencies']['inheritance'] = inheritance_definitions.get(base_class)

            # 方法参数依赖
            param_dependencies = {}
            for method in class_data['methods']:
                param_types = {param['type'] for param in method['parameters']}
                param_definitions = find_definitions(param_types, include_paths)
                param_dependencies[method['name']] = param_definitions  # 按方法存储参数依赖
            
            class_data['dependencies']['parameters'] = param_dependencies

    return parsed_data

def main():
    folder_path = "ability_ability_runtime/interfaces/inner_api/ability_manager/include"
    parsed_file = "parsed_interfaces.json"
    output_file = "enhanced_parsed_interfaces.json"

    with open(parsed_file, 'r', encoding='utf-8') as file:
        parsed_data = json.load(file)

    parsed_data = analyze_dependencies(parsed_data, folder_path)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(parsed_data, file, indent=4, ensure_ascii=False)
    print(f"增强的解析结果已保存到 {output_file}")

if __name__ == "__main__":
    main()