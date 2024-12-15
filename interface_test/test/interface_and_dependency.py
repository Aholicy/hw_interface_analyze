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
                    module_name = os.path.relpath(file_path, api_folder).replace(os.sep, "/").replace(".d.ts", "")
                    
                    # Extract dependencies, interfaces, and method details
                    dependencies = extract_dependencies(content)
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
def extract_dependencies(content):
    dependencies = []
    
    # Match import statements to extract dependencies (including named imports)
    import_matches = re.findall(r"import\s+(\{?[\w,\s]*\}?)\s+from\s+'(.*?)';", content)
    for imports, module in import_matches:
        module = module.replace(".d.ts", "")  # Remove the .d.ts extension
        # Extract named imports (e.g., { AsyncCallback })
        if imports:
            imports = [imp.strip() for imp in imports.replace("{", "").replace("}", "").split(",")]
            for imp in imports:
                dependencies.append({"module": module, "imported_as": imp})
        else:
            dependencies.append({"module": module, "imported_as": module.split("/")[-1]})  # Use last part of module path as alias
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

# Step 6: Create a dependency graph and visualize it
def create_dependency_graph(modules):
    graph = nx.DiGraph()

    # Add edges for dependencies
    for module, data in modules.items():
        for dep in data["dependencies"]:
            graph.add_edge(module, dep["module"])

    return graph

def visualize_graph(graph, output_image):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
    plt.savefig(output_image)
    plt.close()

if __name__ == "__main__":
    # Define input and output paths
    api_folder = "./api/ability"  # Replace with the path to your `api` folder
    output_file = "modules_with_dependencies_and_methods.json"
    dependency_graph_image = "dependency_graph.png"

    # Parse, extract, and save dependencies, methods, and interface properties
    modules = parse_dts_files(api_folder)
    save_data_to_file(modules, output_file)

    # Create and visualize the dependency graph
    graph = create_dependency_graph(modules)
    visualize_graph(graph, dependency_graph_image)

    print("Dependency extraction, method parsing, and visualization complete.")
