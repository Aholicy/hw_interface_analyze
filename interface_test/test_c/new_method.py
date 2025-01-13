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
    
    # 按逗号分隔参数
    params = parameters.split(',')
    for param in params:
        param = param.strip()
        
        if param:
            # 检查是否以 'const' 开头
            const_modifier = ''
            if param.startswith('const'):
                const_modifier = 'const'
                param = param[len(const_modifier):].strip()
            
            # 检查是否有 '&' 符号，如果有，将其分为类型和参数名
            if '&' in param:
                type_part, name_part = param.split('&', 1)
                type_part = type_part.strip() + ' &'  # 包括 '&' 符号作为类型的一部分
                param_name = name_part.strip()
                
                # 如果有 const 修饰符，将其附加到类型前
                if const_modifier:
                    type_part = f"{const_modifier} {type_part}"
                
                param_list.append({'type': type_part, 'name': param_name})
            else:
                # 如果没有 '&' 符号，直接用正则提取类型和名称
                match = re.match(r'([a-zA-Z_][\w:<>*&\s]+)\s+([a-zA-Z_][\w]*)', param)
                if match:
                    param_type = match.group(1).strip()  # 类型
                    param_name = match.group(2).strip()  # 参数名
                    
                    # 如果有 const 修饰符，将其附加到类型前
                    if const_modifier:
                        param_type = f"{const_modifier} {param_type}"
                    
                    param_list.append({'type': param_type, 'name': param_name})
                else:
                    # 无法匹配的情况（例如默认值），直接添加
                    param_list.append({'type': param, 'name': None})
    
    return param_list

# def extract_parameter_types(parameter_string):
#     """精确提取函数参数的类型"""
#     if not parameter_string.strip():
#         return []
#     parameters = parameter_string.split(',')
#     types = []
#     for param in parameters:
#         type_part = re.sub(r'[\w]+$', '', param).strip()  # 去掉变量名，仅保留类型
#         type_part = type_part.replace('*', '').replace('&', '').strip()  # 处理指针和引用
#         types.append(type_part)
#     return types

# def find_definitions(symbols, include_paths):
#     """查找符号定义"""
#     definitions = {}
#     for include_path in include_paths:
#         if not os.path.exists(include_path):
#             continue
#         with open(include_path, 'r', encoding='utf-8') as file:
#             content = file.read()

#         for symbol in symbols:
#             if re.search(r'\b' + re.escape(symbol) + r'\b', content):
#                 definitions[symbol] = include_path
#     return definitions
def find_definitions(symbols, include_paths, checked_files=None):
    """查找符号定义，支持递归查找，并避免重复检查"""
    if checked_files is None:
        checked_files = set()

    definitions = {}

    # 遍历所有include路径
    for include_path in include_paths:
        if not os.path.exists(include_path) or include_path in checked_files:
            continue

        checked_files.add(include_path)

        with open(include_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 查找符号的定义
        for symbol in symbols:
            # 检查符号是否是类、函数或其他符号的定义
            # 类定义
            class_pattern = re.compile(r'class\s+' + re.escape(symbol) + r'\s*\(', re.DOTALL)
            function_pattern = re.compile(r'(\w[\w:<>*&\s]+)\s+' + re.escape(symbol) + r'\s*\(', re.DOTALL)
            enum_pattern = re.compile(r'enum\s+class\s+' + re.escape(symbol) + r'\s*\{', re.DOTALL)

            if class_pattern.search(content):
                definitions[symbol] = include_path
                continue
            elif function_pattern.search(content):
                definitions[symbol] = include_path
                continue
            elif enum_pattern.search(content):
                definitions[symbol] = include_path
                continue

        # 递归查找#includes的文件
        includes = re.findall(r'#include\s+"([\w./]+)"', content)
        # 避免重复检查同一个文件，继续递归寻找定义
        for include in includes:
            # 构建完整路径并递归查找
            include_full_path = os.path.join(os.path.dirname(include_path), include)
            if include_full_path not in checked_files:
                nested_definitions = find_definitions(symbols, [include_full_path], checked_files)
                definitions.update(nested_definitions)

    return definitions


def analyze_dependencies(parsed_data, folder_path):
    """分析继承类和函数参数类型的依赖"""
    all_includes = set()

    # 常见类型排除列表
    exclude_types = {'int', 'int32_t', 'int64_t', 'float', 'double', 'char', 'bool', 'short', 'long', 'string', 'std::string','uint64_t'}

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

            # 方法参数依赖，排除常见类型
            param_dependencies = {}
            for method in class_data['methods']:
                param_types = {param['type'] for param in method['parameters']}

                param_types = {ptype[5:] if ptype.startswith('const') else ptype for ptype in param_types}
                param_types = {ptype[:-1] if ptype.endswith('&') else ptype for ptype in param_types}

                # 提取尖括号内的内容
                extracted_types = set()
                for ptype in param_types:
                    match = re.search(r'<(.*?)>', ptype)
                    if match:
                        extracted_types.add(match.group(1))
                param_types.update(extracted_types)

                # 去除空格内容
                param_types = {ptype.strip() for ptype in param_types}
                # 过滤掉常见类型
                param_types = {ptype for ptype in param_types if ptype.split()[0] not in exclude_types}

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
