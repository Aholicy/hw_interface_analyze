import json
import re

def extract_namespace_dependencies(parsed_data):
    """提取命名空间相关的依赖关系"""
    namespace_dependencies = {}

    # 遍历模块
    for module_name, module_data in parsed_data.items():
        # 如果该模块包含类信息，则继续处理
        if 'classes' in module_data:
            for class_name, class_data in module_data['classes'].items():
                # 遍历该类的所有方法
                for method in class_data['methods']:
                    # 提取方法的参数
                    parameters = method['parameters']
                    # 使用正则表达式提取参数中的命名空间
                    matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*::[a-zA-Z_][a-zA-Z0-9_]*)', parameters)
                    for match in matches:
                        # 提取命名空间部分
                        namespace = match.split('::')[0]
                        if namespace not in namespace_dependencies:
                            namespace_dependencies[namespace] = set()
                        # 将当前模块的头文件依赖添加到命名空间依赖中
                        namespace_dependencies[namespace].update(module_data['includes'])
                    
                    # 还可以检查方法名中的命名空间（如果有的话）
                    if '::' in method['name']:
                        namespace_in_method_name = method['name'].split('::')[0]
                        if namespace_in_method_name not in namespace_dependencies:
                            namespace_dependencies[namespace_in_method_name] = set()
                        namespace_dependencies[namespace_in_method_name].update(module_data['includes'])

    # 将 set 转换为 list，确保可以序列化为 JSON
    for namespace, includes in namespace_dependencies.items():
        namespace_dependencies[namespace] = list(includes)

    return namespace_dependencies

def main():
    # 从文件读取已解析的JSON数据
    with open('parsed_interfaces.json', 'r', encoding='utf-8') as file:
        parsed_data = json.load(file)

    # 提取命名空间相关的依赖
    namespace_deps = extract_namespace_dependencies(parsed_data)

    # 打印或保存命名空间依赖
    with open('namespace_dependencies.json', 'w', encoding='utf-8') as file:
        json.dump(namespace_deps, file, indent=4, ensure_ascii=False)
    
    print("命名空间依赖已保存到 'namespace_dependencies.json'")

if __name__ == "__main__":
    main()
