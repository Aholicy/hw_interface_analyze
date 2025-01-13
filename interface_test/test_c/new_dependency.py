import os
import re
import json

def find_definitions(symbols, modules):
    """从模块的 classes, enums 和 methods 中查找符号定义"""
    definitions = {}

    for module_name, module_data in modules.items():
        # 获取模块中的enums和classes
        enums = module_data.get('enums', [])
        classes = module_data.get('classes', {})

        # 查找枚举定义
        for enum in enums:
            if enum['name'] in symbols:
                definitions[enum['name']] = module_name
        
        # 查找类定义
        for class_name, class_data in classes.items():
            if class_name in symbols:
                definitions[class_name] = module_name

            # 查找类方法中的符号
            for method in class_data['methods']:
                if method['name'] in symbols:
                    definitions[method['name']] = module_name

    return definitions

def collect_includes(module_name, parsed_data, checked_modules=None):
    """递归收集所有include的模块名"""
    if checked_modules is None:
        checked_modules = set()

    checked_modules.add(module_name)
    includes = parsed_data.get(module_name, {}).get('includes', [])
    all_includes = set(includes)  # 保存当前模块的所有includes

    for include in includes:
        # 对于每个include，递归查找
        if include not in checked_modules:
            checked_modules.add(include)
            # 如果该include的模块存在，递归获取该模块的includes
            if include in parsed_data:
                all_includes.update(collect_includes(include, parsed_data, checked_modules))

    return all_includes

def analyze_dependencies(parsed_data):
    """分析继承类和函数参数类型的依赖"""
    missing_includes = set()

    # 常见类型排除列表
    exclude_types = {'int', 'int32_t', 'int64_t', 'float', 'double', 'char', 'bool', 'short', 'long', 'string', 'std::string', 'uint64_t'}

    # 遍历每个模块，获取它们的依赖
    print(parsed_data.keys())
    for module_name, data in parsed_data.items():
        # 获取该模块的所有递归includes
        all_includes = collect_includes(module_name, parsed_data)

        # 建立一个新的字典，保存parsed_data.keys中所有的数据去除/前半部分的名称
        new_parsed_data = {}
        for key in parsed_data.keys():
            new_parsed_data[key.split('/')[-1]] = parsed_data[key]
        # 检查模块中的每个include是否在parsed_data中存在
        for include in all_includes:
            include = include.replace('.h', '')
            # 如果模块名本身不在parsed_data中，或者去掉路径后的模块名不在parsed_data中
            include_base_name = include.split('/')[-1]  # 去掉路径后的模块名
            if include not in parsed_data.keys() and include_base_name not in new_parsed_data:
                print(f"缺失的include: {include}")
                missing_includes.add(include)

        for class_name, class_data in data['classes'].items():
            if 'dependencies' not in class_data:
                class_data['dependencies'] = {'inheritance': {}, 'parameters': {}}

            # 继承类依赖
            base_class = class_data['base_class']
            if base_class:
                inheritance_definitions = find_definitions([base_class], parsed_data)
                if inheritance_definitions:
                    # 找到继承的模块及类
                    base_class_module = inheritance_definitions.get(base_class)
                    class_data['dependencies']['inheritance'] = {
                        'class': class_name,
                        'base_class': base_class,
                        'base_class_module': base_class_module
                    }
                else:
                    # 没有找到依赖文件，保持为空
                    class_data['dependencies']['inheritance'] = {
                        'class': class_name,
                        'base_class': base_class,
                        'base_class_module': None
                    }

            # 方法参数依赖，排除常见类型                       
            param_dependencies = {}
            for method in class_data['methods']:
                param_types = {param['type'] for param in method['parameters']}

                # 处理 const 和 & 符号
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

                # 优先在当前模块中查找定义
                local_definitions = find_definitions(list(param_types), {module_name: data})
                unresolved_types = {ptype for ptype in param_types if ptype not in local_definitions}

                # 对未找到的类型在全局模块中查找
                global_definitions = find_definitions(list(unresolved_types), parsed_data)
                unresolved_types = {ptype for ptype in unresolved_types if ptype not in global_definitions}

                # 按优先级存储结果
                param_dependencies[method['name']] = {
                    'local': local_definitions,           # 当前模块中找到的类型
                    'global': global_definitions,         # 全局模块中找到的类型及模块名
                    'unresolved': list(unresolved_types)  # 未解析的类型
                }
            
            class_data['dependencies']['parameters'] = param_dependencies


    return parsed_data, missing_includes

def main():
    parsed_file = "parsed_interfaces.json"
    output_file = "enhanced_parsed_interfaces2.json"
    missing_file = "missing_includes.json"

    # 加载已解析的数据
    with open(parsed_file, 'r', encoding='utf-8') as file:
        parsed_data = json.load(file)

    # 分析依赖关系并获取缺失的includes
    parsed_data, missing_includes = analyze_dependencies(parsed_data)

    # 保存分析结果
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(parsed_data, file, indent=4, ensure_ascii=False)

    # 保存missing_includes
    with open(missing_file, 'w', encoding='utf-8') as file:
        json.dump(list(missing_includes), file, indent=4, ensure_ascii=False)

    print(f"增强的解析结果已保存到 {output_file}")
    print(f"缺失的includes已保存到 {missing_file}")

if __name__ == "__main__":
    main()
