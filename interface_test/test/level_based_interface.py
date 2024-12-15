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
                    dependencies = extract_dependencies(content, root, api_folder)  # Pass the current root and api_folder
                    interfaces = extract_interface_properties(content)
                    methods = extract_methods(content)

                    # Store module data
                    modules[module_name] = {
                        "dependencies": dependencies,
                        "interfaces": interfaces,
                        "methods": methods
                    }

    return modules

# Step 2: Extract dependencies from file content
def extract_dependencies(content, current_dir, api_folder):
    dependencies = []
    
    # Match import statements to extract dependencies (including named imports)
    import_matches = re.findall(r"import\s+(\{?[\w,\s]*\}?)\s+from\s+'(.*?)';", content)
    for imports, module in import_matches:
        # Fix relative paths like '../' or './' based on current directory
        original_module = module  # Save original module for later use
        if module.startswith("./"):
            module = module[2:]
        while module.startswith("../"):
            # 如果出现 '../'，则将 current_dir 向上一层
            current_dir = os.path.dirname(current_dir)
            # 移除模块路径中的 '../'
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
                dependencies.append({"module": module_path, "imported_as": imp})
        else:
            # Use last part of module path as alias if no imports found
            dependencies.append({"module": module_path, "imported_as": original_module.split("/")[-1]})

    return dependencies


# Step 3: Extract interface properties from file content
def extract_interface_properties(content):
    interfaces = {}
    
    # Match interfaces and their properties
    interface_matches = re.finditer(r"interface\s+(\w+)\s+\{([^}]*)\}", content, re.DOTALL)
    
    for match in interface_matches:
        interface_name = match.group(1)
        properties_block = match.group(2)
        
        # Extract properties of each interface
        properties = re.findall(r"(\w+)\s*:\s*[^;]+;", properties_block)
        interfaces[interface_name] = properties

    return interfaces

# Step 4: Extract method details from file content (including exceptions, parameters, and return types)
def extract_methods(content):
    methods = []

    # Match method signatures and descriptions
    method_matches = re.finditer(r"(\w+)\s+(\w+)\s?\(([^)]*)\)\s*:\s*([\w<>]+)\s*(//.*)?", content)

    for match in method_matches:
        method_name = match.group(2)
        return_type = match.group(4)
        params_str = match.group(3)
        comment_block = match.group(5)

        # Extract parameters (name and type)
        params = []
        if params_str:
            param_matches = re.findall(r"(\w+):\s*(\w+)", params_str)
            for param_name, param_type in param_matches:
                params.append({"name": param_name, "type": param_type})

        # Extract exceptions
        exceptions = []
        if comment_block:
            exception_matches = re.findall(r"@throws\s+{(\w+)}\s+(\d+)\s+-\s+(.+)", comment_block)
            for exc_type, exc_code, exc_desc in exception_matches:
                exceptions.append({
                    "type": exc_type,
                    "code": exc_code,
                    "description": exc_desc
                })
        
        # Store method details
        methods.append({
            "method_name": method_name,
            "return_type": return_type,
            "parameters": params,
            "exceptions": exceptions
        })

    return methods

# Step 5: Save all data into a JSON file
def save_data_to_file(modules, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(modules, f, indent=4)

# Step 6: Create a dependency graph and visualize it with groupings
def create_dependency_graph(modules):
    graph = nx.DiGraph()

    # Add edges for dependencies
    for module, data in modules.items():
        for dep in data["dependencies"]:
            graph.add_edge(module, dep["module"])

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
    plt.close()

if __name__ == "__main__":
    # Define input and output paths
    api_folder = "./api"  # Replace with the path to your `api` folder
    output_file = "modules_with_dependencies_and_methods.json"
    dependency_graph_image = "dependency_graph.png"

    # Parse, extract, and save dependencies, methods, and interface properties
    modules = parse_dts_files(api_folder)
    save_data_to_file(modules, output_file)

    # Create and visualize the dependency graph
    graph = create_dependency_graph(modules)
    visualize_graph(graph, dependency_graph_image, modules)

    print("Dependency extraction, method parsing, and visualization complete.")
