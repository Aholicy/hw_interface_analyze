import os
import re
import json
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Parse .d.ts files
def parse_dts_files(api_folder):
    modules = {}

    # Traverse the api folder recursively
    for root, _, files in os.walk(api_folder):
        for file in files:
            if file.endswith(".d.ts"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    module_name = os.path.relpath(file_path, api_folder).replace(os.sep, ".").replace(".d.ts", "")
                    
                    # Extract dependencies, interfaces, and method details
                    dependencies = extract_dependencies(content, root, api_folder)
                    interfaces = extract_interface_properties(content)
                    methods = extract_methods(content)
                    class_inheritance = extract_inheritance(content)

                    # Store module data
                    modules[module_name] = {
                        "dependencies": dependencies,
                        "interfaces": interfaces,
                        "methods": methods,
                        "inheritance": class_inheritance
                    }

    return modules

# Step 2: Extract dependencies from file content
def extract_dependencies(content, current_dir, api_folder):
    dependencies = []
    
    # Match import statements to extract dependencies (including named imports)
    import_matches = re.findall(r"import\s+(?:\* as\s+(\w+)\s+from\s+|(?:\{?[\w,\s]*\}?)\s+from\s+)['\"](.*?)['\"];", content)
    for imports, module in import_matches:
        # Handling * imports (e.g. import * as PacMap from ...), and named imports with alias (e.g. import { Y as Z })
        if imports:
            # For `import * as X from ...`
            dependencies.append({
                "original_module": module,
                "imported_as": imports
            })
        else:
            # Handle relative paths and absolute paths correctly
            original_module = module
            if module.startswith("./"):
                module = module[2:]
            while module.startswith("../"):
                current_dir = os.path.dirname(current_dir)
                module = module.replace('../', '', 1)
            
            # Build absolute path for the module based on current file's folder and relative path
            module_path = os.path.join(current_dir, module).replace(api_folder, "").replace(os.sep, ".").replace(".d.ts", "")
            
            # Remove './' at the beginning of the relative path and fix internal module references
            if module_path.startswith("./"):
                module_path = module_path[2:]
            while module_path.startswith("."):
                module_path = module_path[1:]

            # Add '@ohos' prefix only if the module path doesn't already start with '@ohos'
            if not module_path.startswith("@ohos"):
                module_path = "@ohos." + module_path

            # Extract named imports (e.g., { AsyncCallback })
            if imports:
                imports = [imp.strip() for imp in imports.replace("{", "").replace("}", "").split(",")]
                for imp in imports:
                    dependencies.append({
                        "original_module": module_path,
                        "imported_as": imp
                    })
            else:
                dependencies.append({
                    "original_module": module_path,
                    "imported_as": original_module.split("/")[-1]
                })

    return dependencies


def extract_interface_properties(content):
    interfaces = {}

    # 匹配接口和类型别名，支持更复杂的结构
    interface_matches = re.finditer(r"(interface|type)\s+(\w+)\s*\{([^}]*)\}", content, re.DOTALL)

    for match in interface_matches:
        interface_name = match.group(2)
        properties_block = match.group(3)

        # 提取接口的属性
        properties = re.findall(r"(\w+)\s*:\s*([^;]+);", properties_block)
        interfaces[interface_name] = properties

    # 处理 typedef 类型的别名
    typedef_matches = re.finditer(r"@typedef\s+{([^}]+)}\s+(\w+)", content)
    for match in typedef_matches:
        alias_type = match.group(1)  # 被别名化的类型
        alias_name = match.group(2)  # 别名名称
        interfaces[alias_name] = [alias_type]  # 别名指向原始类型

    return interfaces



# Step 4: Extract method details from file content (including exceptions, parameters, and return types)
def extract_methods(content):
    methods = []
    functions = []
    class_attributes = {}

    # 提取类中的方法（无论是否有 export 和 default）
    class_method_matches = re.finditer(
        r"(?:export\s+default\s+class\s+|export\s+class\s+)(\w+)[^{]*{([\s\S]*?)}", content
    )
    
    for class_match in class_method_matches:
        class_name = class_match.group(1)
        class_methods_content = class_match.group(2)

        # 提取类的属性（例如 context: DriverExtensionContext）
        attribute_matches = re.findall(r"\s*(\w+)\s*:\s*([\w<>\[\]]+)", class_methods_content)
        class_attributes[class_name] = [{"name": attr[0], "type": attr[1]} for attr in attribute_matches]

        # 提取类中的方法，包括静态方法和实例方法
        method_matches = re.finditer(
            r"(static\s+)?(\w+)\s+(\w+)\s?\(([^)]*)\)\s*:\s*([\w<>\|\[\]]+(\s*\|\s*[\w<>\|\[\]]+)*)\s*(?=\s*(?:;|\{|\s*\*{0}))", class_methods_content
        )
        
        for match in method_matches:
            is_static = bool(match.group(1))  # 是否是静态方法
            method_name = match.group(3)  # 方法名
            return_type = match.group(5)  # 返回类型
            params_str = match.group(4)  # 参数字符串

            # 提取参数（名称和类型）
            params = []
            if params_str:
                param_matches = re.findall(r"(\w+):\s*([\w<>\|\[\]]+)", params_str)  # 支持复杂类型
                for param_name, param_type in param_matches:
                    params.append({"name": param_name, "type": param_type})

            methods.append({
                "class": class_name,
                "is_static": is_static,
                "method_name": method_name,
                "return_type": return_type,
                "parameters": params
            })

    # 提取全局函数
    function_matches = re.finditer(
        r"function\s+(\w+)\s?\(([^)]*)\)\s*:\s*([\w<>\|\[\]]+(\s*\|\s*[\w<>\|\[\]]+)*)", content
    )
    
    for match in function_matches:
        function_name = match.group(1)
        params_str = match.group(2)
        return_type = match.group(3)

        # 提取参数（名称和类型）
        params = []
        if params_str:
            param_matches = re.findall(r"(\w+):\s*([\w<>\|\[\]]+)", params_str)
            for param_name, param_type in param_matches:
                params.append({"name": param_name, "type": param_type})

        functions.append({
            "function_name": function_name,
            "return_type": return_type,
            "parameters": params
        })
    
    # 额外的正则表达式：用于识别所有的函数声明（包括方法体）
    method_body_matches = re.finditer(
        r"(\w+)\s?\(([^)]*)\)\s*:\s*([\w<>\|\[\]]+(\s*\|\s*[\w<>\|\[\]]+)*)\s*(?=\s*({|;))", content
    )
    
    for match in method_body_matches:
        method_name = match.group(1)  # 方法名
        params_str = match.group(2)   # 参数字符串
        return_type = match.group(3)  # 返回类型

        # 提取参数（名称和类型）
        params = []
        if params_str:
            param_matches = re.findall(r"(\w+):\s*([\w<>\|\[\]]+)", params_str)
            for param_name, param_type in param_matches:
                params.append({"name": param_name, "type": param_type})

        methods.append({
            "method_name": method_name,
            "return_type": return_type,
            "parameters": params
        })

    # 返回时将类的属性和方法一起返回
    for method in methods:
        if "class" in method:
            class_name = method["class"]
            method["class_attributes"] = class_attributes.get(class_name, [])

    return {"functions": functions, "methods": methods}



# Step 5: Extract class inheritance (extends)
def extract_inheritance(content):
    inheritance = []

    # Match classes and their inheritance (extends)
    class_matches = re.finditer(r"(?:export\s+default\s+class\s+|export\s+class\s+)(\w+)(?:\s+extends\s+([\w.]+))?", content)
    
    for match in class_matches:
        class_name = match.group(1)
        base_class = match.group(2) if match.group(2) else None
        
        # If it's a default class, we handle it differently and add methods to it
        inheritance.append({"class": class_name, "extends": base_class})

    return inheritance

# Step 6: Save all data into a JSON file
def save_data_to_file(modules, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(modules, f, indent=4)

# Step 7: Create a dependency graph and visualize it with groupings
def create_dependency_graph(modules):
    graph = nx.DiGraph()

    # Add edges for dependencies
    for module, data in modules.items():
        for dep in data["dependencies"]:
            graph.add_edge(module, dep["original_module"])

    return graph

def group_modules(modules):
    # Group modules based on some attribute, e.g., by module folder or interface
    groups = {}
    for module, data in modules.items():
        # For simplicity, we group by the first part of the module name
        group_name = module.split("/")[0]
        if group_name not in groups:
            groups[group_name] = []
        groups[group_name].append(module)

    return groups

import random

def visualize_graph(graph, output_image, modules):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    
    # Group nodes and color them accordingly
    groups = group_modules(modules)
    
    # Generate a unique color for each group
    group_colors = {group: [random.random(), random.random(), random.random()] for group in groups}  # Random colors for each group
    
    node_colors = []
    node_labels = {}
    
    for node in graph.nodes:
        group_name = node.split("/")[0]  # Simplified grouping by module folder name
        node_colors.append(group_colors.get(group_name, [0.5, 0.5, 0.5]))  # Default to gray if no group found
        node_labels[node] = node.split("/")[-1]  # Display only the last part of the module name for clarity
    
    nx.draw(graph, pos, with_labels=True, labels=node_labels, node_size=3000, node_color=node_colors, font_size=10, font_weight="bold", alpha=0.7)
    plt.savefig(output_image)
    plt.show()

# Example usage
api_folder = "./api"
output_file = "output_modules.json"
dependency_graph_image = "dependency_graph.png"

modules = parse_dts_files(api_folder)
save_data_to_file(modules, output_file)

graph = create_dependency_graph(modules)
visualize_graph(graph, dependency_graph_image, modules)

print("Dependency extraction, method parsing, and visualization complete.")
