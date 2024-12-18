import json

# 假设你的 JSON 文件保存在同一个目录下，文件名为 'project.json'
def load_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def find_dependencies(data, target_module, path=None):
    """
    递归查找所有依赖于目标模块的组件。
    :param data: 当前组件的字典
    :param target_module: 目标模块
    :param path: 组件的路径（用于显示组件层级）
    :return: 返回所有依赖于目标模块的组件路径
    """
    if path is None:
        path = []

    dependent_components = []

    # 检查当前组件是否依赖于目标模块
    if "dependencies" in data:
        for dep in data["dependencies"]:
            if isinstance(dep, dict) and 'module' in dep:
                if dep['module'] == target_module:
                    dependent_components.append({
                        "component": '.'.join(path),
                        "dependency": dep
                    })

    # 递归查找子组件
    for key, value in data.items():
        if isinstance(value, dict):  # 如果是子组件，继续递归
            dependent_components.extend(find_dependencies(value, target_module, path + [key]))

    return dependent_components

def display_dependencies(dependencies):
    """
    格式化输出依赖于目标模块的组件信息。
    :param dependencies: 依赖信息列表
    """
    if not dependencies:
        print("没有找到依赖于目标模块的组件。")
        return

    for dep in dependencies:
        component = dep['component']
        dependency = dep['dependency']
        print(f"组件: {component} -> 依赖于 {dependency['module']} (通过导入为 {dependency.get('imported_as', 'N/A')})")

if __name__ == "__main__":
    # 加载 JSON 文件
    json_data = load_json_file('dependencies_analysis.json')

    # 设置目标模块
    target_module = "@ohos.multimedia.image"  # 例如 B 模块

    # 查找所有依赖于目标模块的组件
    dependencies = find_dependencies(json_data, target_module)

    # 输出依赖信息
    display_dependencies(dependencies)
