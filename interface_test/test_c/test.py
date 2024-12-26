import os
import re
import json

def parse_header_file(file_path, module_name):
    """解析头文件并提取接口和依赖关系"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 提取依赖的头文件
    includes = re.findall(r'#include\s+"([\w./]+)"', content)

    # 提取枚举类信息
    enums = []
    enum_pattern = re.compile(r'enum\s+class\s+(\w+)\s*\{([^}]*)\}', re.DOTALL)
    for match in enum_pattern.finditer(content):
        enum_name = match.group(1).strip()
        enum_values = []

        # 提取枚举值
        enum_lines = match.group(2).split(',')

        for enum_value in enum_lines:
            enum_value = enum_value.strip()
            # 清理行内注释（例如 // ipc id 1-1000 for kit）
            enum_value_clean = re.sub(r'//.*', '', enum_value).strip()

            if enum_value_clean:  # 只处理非空的枚举值
                parts = enum_value_clean.split('=')
                value = parts[0].strip()
                ipc_id = parts[1].strip() if len(parts) > 1 else None
                enum_dict = {
                    'name': value,
                    'ipc_id': ipc_id
                }
                enum_values.append(enum_dict)

        enums.append({
            'name': enum_name,
            'values': enum_values
        })

    # 提取类信息和方法
    classes = {}
    class_pattern = re.compile(r'class\s+(\w+)\s*(?::\s*public\s+([\w:]+))?\s*\{([^}]*)\}', re.DOTALL)
    for class_match in class_pattern.finditer(content):
        class_name = class_match.group(1).strip()
        base_class = class_match.group(2).strip() if class_match.group(2) else None
        class_body = class_match.group(3).strip()

        # 提取类方法
        method_pattern = re.compile(
            r'([a-zA-Z_][a-zA-Z0-9_ ]*\s+\*?\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*(const|override|= 0)?\s*;'
        )
        methods = []
        for method_match in method_pattern.finditer(class_body):
            return_type = method_match.group(1).strip()
            method_name = method_match.group(2).strip()
            parameters = method_match.group(3).strip()
            is_const = method_match.group(4) is not None

            # 解析参数，提取类型和名称
            param_list = parse_parameters(parameters)

            methods.append({
                'name': method_name,
                'return_type': return_type,
                'parameters': param_list,
                'is_const': is_const
            })

        # 提取使用了命名空间的成员（通过 "::" 符号）
        namespace_uses = extract_namespace_uses(class_body)

        classes[class_name] = {
            'base_class': base_class,
            'methods': methods,
            'namespace_uses': namespace_uses,
        }

    # 提取命名空间
    namespaces = extract_namespaces(content)

    # 提取顶级 namespace 使用
    namespace_uses = extract_namespace_uses(content)

    return {
        'module': module_name,
        'includes': includes,
        'enums': enums,
        'classes': classes,
        'namespaces': namespaces,
        'namespace_uses': namespace_uses  # 确保字段存在
    }

def extract_namespaces(content):
    """提取文件中的所有命名空间（包括嵌套的命名空间）"""
    namespaces = []
    namespace_pattern = re.compile(r'namespace\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\{')
    for match in namespace_pattern.finditer(content):
        namespaces.append(match.group(1).strip())
    return namespaces

def extract_namespace_uses(content):
    """提取文件中使用了命名空间的所有符号，去重"""
    namespace_uses = set()  # 使用集合避免重复
    use_pattern = re.compile(r'\b([a-zA-Z_][\w:]+)::')
    for match in use_pattern.finditer(content):
        namespace_uses.add(match.group(1).strip())  # 添加到集合
    return list(namespace_uses)  # 转为列表返回

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

def parse_folder(folder_path, module_prefix=""):
    """递归解析文件夹中的头文件和子文件夹"""
    result = {}
    for entry in os.scandir(folder_path):
        if entry.is_dir():
            # 子文件夹处理
            sub_module_prefix = f"{module_prefix}.{entry.name}" if module_prefix else entry.name
            result.update(parse_folder(entry.path, sub_module_prefix))
        elif entry.is_file() and entry.name.endswith('.h'):
            # 头文件处理
            module_name = f"{module_prefix}.{entry.name[:-2]}" if module_prefix else entry.name[:-2]
            result[module_name] = parse_header_file(entry.path, module_name)
    return result

def main():
    folder_path = "ability_ability_runtime/interfaces/inner_api/ability_manager/include"  # 根文件夹路径
    output_file = "parsed_interfaces.json"  # 输出文件路径

    # 解析文件夹
    parsed_data = parse_folder(folder_path)

    # 保存为JSON
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(parsed_data, file, indent=4, ensure_ascii=False)
    print(f"解析结果已保存到 {output_file}")

if __name__ == "__main__":
    main()
