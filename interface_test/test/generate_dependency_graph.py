import os
import re
import json
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Parse .d.ts files
def parse_dts_files(api_folder):
    dependencies = {}

    for root, _, files in os.walk(api_folder):
        for file in files:
            if file.endswith(".d.ts"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    module_name = os.path.relpath(file_path, api_folder).replace(os.sep, "/").replace(".d.ts", "")
                    dependencies[module_name] = extract_dependencies(content)

    return dependencies

# Step 2: Extract dependencies from file content
def extract_dependencies(content):
    imports = re.findall(r"import\s+.*?from\s+'(.*?)';", content)
    return [import_path.replace(".d.ts", "") for import_path in imports]

# Step 3: Save dependencies as a JSON file
def save_dependencies_to_file(dependencies, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dependencies, f, indent=4)

# Step 4: Create a dependency graph and visualize
def create_dependency_graph(dependencies):
    graph = nx.DiGraph()

    for module, deps in dependencies.items():
        for dep in deps:
            graph.add_edge(module, dep)

    return graph

def visualize_graph(graph, output_image):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
    plt.savefig(output_image)
    plt.close()

if __name__ == "__main__":
    # Define input and output paths
    api_folder = "./api"  # Replace with the path to your `api` folder
    dependencies_file = "dependencies.json"
    dependency_graph_image = "dependency_graph.png"

    # Parse, extract, and save dependencies
    dependencies = parse_dts_files(api_folder)
    save_dependencies_to_file(dependencies, dependencies_file)

    # Create and visualize dependency graph
    graph = create_dependency_graph(dependencies)
    visualize_graph(graph, dependency_graph_image)

    print("Dependency extraction and visualization complete.")
