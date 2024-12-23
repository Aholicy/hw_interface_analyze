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

        # 清理枚举值中的注释并提取有效的枚举值和IPC ID
        enum_lines = match.group(2).split(',')
        current_comment = None  # 存储当前的注释内容

        for enum_value in enum_lines:
            enum_value = enum_value.strip()

            # 如果这行是注释行（以 // 开头），提取注释内容并跳过它
            if enum_value.startswith("//"):
                current_comment = enum_value.lstrip("//").strip()  # 存储注释内容
                continue  # 跳过注释行

            # 清理行内注释（例如 // ipc id 1-1000 for kit）
            enum_value_clean = re.sub(r'//.*$', '', enum_value).strip()

            if enum_value_clean:  # 只处理非空的枚举值
                parts = enum_value_clean.split('=')
                value = parts[0].strip()
                ipc_id = parts[1].strip() if len(parts) > 1 else None
                enum_dict = {
                    'name': value,
                    'ipc_id': ipc_id
                }
                # 如果有注释，存储在当前枚举值的 `comment` 字段中
                if current_comment:
                    enum_dict['comment'] = current_comment
                    current_comment = None  # 清空注释内容
                enum_values.append(enum_dict)

        enums.append({
            'name': enum_name,
            'values': enum_values
        })

    # 提取类信息和方法
    classes = {}
    class_pattern = re.compile(r'class\s+(\w+)\s*(?::\s*public\s+\w+)?\s*\{([^}]*)\}', re.DOTALL)
    for class_match in class_pattern.finditer(content):
        class_name = class_match.group(1).strip()
        class_body = class_match.group(2).strip()

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

            methods.append({
                'name': method_name,
                'return_type': return_type,
                'parameters': parameters,
                'is_const': is_const
            })

        # 将类方法与接口方法结合起来
        interfaces = []
        interface_pattern = re.compile(
            r'([a-zA-Z_][a-zA-Z0-9_ ]*\s+\*?\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*;'
        )
        for match in interface_pattern.finditer(content):
            return_type = match.group(1).strip()
            interface_name = match.group(2).strip()
            parameters = match.group(3).strip()

            # 检查是否属于当前类
            if interface_name not in [m['name'] for m in methods]:
                interfaces.append({
                    'name': interface_name,
                    'return_type': return_type,
                    'parameters': parameters
                })

        classes[class_name] = {
            'methods': methods,
            'interfaces': interfaces
        }

    return {
        'module': module_name,
        'includes': includes,
        'enums': enums,
        'classes': classes
    }

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
