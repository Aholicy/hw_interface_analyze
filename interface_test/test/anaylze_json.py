import json
import os

def analyze_dependencies(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    dependencies = {}
    
    for module, details in data.items():
        parts = module.split('.')
        current_level = dependencies
        
        for part in parts:
            if part not in current_level:
                current_level[part] = {"dependencies": [], "interfaces": {}, "methods": []}
            current_level = current_level[part]
        
        current_level["dependencies"] = details.get("dependencies", [])
        current_level["interfaces"] = details.get("interfaces", {})
        current_level["methods"] = details.get("methods", [])
    
    return dependencies

def save_dependencies(dependencies, output_path):
    with open(output_path, 'w') as file:
        json.dump(dependencies, file, indent=4)

if __name__ == "__main__":
    input_file = '/home/user/yzb/interface_test/test/modules_with_dependencies_and_methods.json'
    output_file = '/home/user/yzb/interface_test/test/dependencies_analysis.json'
    
    dependencies = analyze_dependencies(input_file)
    save_dependencies(dependencies, output_file)
    print(f"Dependencies analysis saved to {output_file}")