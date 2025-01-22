import os
import json
import networkx as nx
import matplotlib.pyplot as plt


def load_json_files_from_directory(directory):
    """加载目录中的所有 JSON 文件"""
    json_files = []
    print(f"Scanning directory: {directory}")  # 调试输出
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    json_files.append((root, file, json_data))
    print(f"Found {len(json_files)} JSON files.")  # 调试输出
    return json_files


def extract_dependencies_from_json(json_data):
    """从 JSON 数据中提取依赖关系"""
    dependencies = []

    # 定义依赖类型
    cursor_kind_map = {
        "TYPE_REF": "CursorKind.TYPE_REF",
        "NAMESPACE_REF": "CursorKind.NAMESPACE_REF",
        "TEMPLATE_REF": "CursorKind.TEMPLATE_REF",
        "MEMBER_REF": "CursorKind.MEMBER_REF",
        "VARIABLE_REF": "CursorKind.VARIABLE_REF",
        "CXX_BASE_SPECIFIER": "CursorKind.CXX_BASE_SPECIFIER",
        "OVERLOADED_DECL_REF": "CursorKind.OVERLOADED_DECL_REF",
        "CALL_EXPR": "CursorKind.CALL_EXPR"
    }

    if json_data:
        print(f"Extracting dependencies from {len(json_data)} nodes.")  # 调试输出

    for node in json_data:
        if "reference_info" in node and node["reference_info"]:
            ref_info = node["reference_info"]
            referenced = ref_info.get("referenced", {})

            # 获取 source_class 和 source_namespace
            source_class = None
            source_namespace = None
            if "class" in ref_info and ref_info["class"]:
                source_class = ref_info["class"].get("name")
            if not source_class and "namespace" in ref_info and ref_info["namespace"]:
                source_namespace = ref_info["namespace"].get("name")

            source_function = None
            if "function" in ref_info and ref_info["function"]:
                source_function = ref_info["function"].get("name")

            # 获取 target_class
            target_class = None
            if referenced and referenced.get("kind") in ["CursorKind.ENUM_DECL", "CursorKind.CLASS_DECL", "CursorKind.STRUCT_DECL"]:
                target_class = referenced.get("name")
            elif referenced.get("parent") and referenced["parent"].get("kind") in ["CursorKind.ENUM_DECL", "CursorKind.CLASS_DECL", "CursorKind.STRUCT_DECL"]:
                target_class = referenced["parent"].get("name")

            # 排除标准库依赖
            if target_class and target_class in ["std", "std::", "uint32_t", "uint64_t", "int32_t", "int64_t", "std::string", "std::vector", "std::map", "std::unordered_map", "std::list", "std::set", "std::unordered_set"]:
                continue

            # 获取依赖类型
            dep_kind = None
            if "self" in ref_info and ref_info["self"]:
                self_info = ref_info["self"]
                dep_kind = self_info.get("kind")

                # 如果self节点的kind属性属于我们指定的类型之一
                if dep_kind in cursor_kind_map:
                    dep_kind = cursor_kind_map[dep_kind]

            # 如果有有效的source_class/namespace 和 target_class
            if (source_class or source_namespace) and target_class:
                dependencies.append({
                    "source_namespace": source_namespace,
                    "source_class": source_class,
                    "source_function": source_function,
                    "target_class": target_class,
                    "kind": dep_kind,  # 保存依赖的类型
                })

    # # 去重：只保留唯一的依赖关系
    # unique_dependencies = []
    # seen = set()
    # for dep in dependencies:
    #     dep_tuple = (dep["source_class"] or dep["source_namespace"], dep["target_class"], dep["kind"], dep["source_function"])
    #     if dep_tuple not in seen:
    #         seen.add(dep_tuple)
    #         unique_dependencies.append(dep)

    # print(f"Extracted {len(unique_dependencies)} unique dependencies.")  # 调试输出
    return dependencies


def generate_dependency_graph(json_files):
    """生成每个文件夹的依赖图"""
    folder_dependencies = {}

    for folder, _, json_data in json_files:
        dependencies = extract_dependencies_from_json(json_data)
        if dependencies:
            # 将每个文件夹的依赖单独保留
            if folder not in folder_dependencies:
                folder_dependencies[folder] = []
            folder_dependencies[folder].extend(dependencies)
    
    print(f"Generated dependency graph for {len(folder_dependencies)} folders.")  # 调试输出
    return folder_dependencies


def save_dependency_graph(folder_dependencies, output_dir):
    """保存依赖图到文件夹，每个文件夹一个依赖图"""
    for folder, dependencies in folder_dependencies.items():
        # 创建文件夹路径
        relative_folder = os.path.relpath(folder, start="ref_ana")  # 依赖分析输出文件夹的根目录
        output_folder = os.path.join(output_dir, relative_folder)

        # 打印调试信息
        print(f"Output folder: {output_folder}")  # 调试输出

        os.makedirs(output_folder, exist_ok=True)

        # 按照kind分类保存依赖
        kind_dependencies = {}
        for dep in dependencies:
            kind = dep["kind"]
            if kind not in kind_dependencies:
                kind_dependencies[kind] = []
            kind_dependencies[kind].append(dep)

        # 保存每个kind类型的依赖到单独的 JSON 文件
        for kind, dep_list in kind_dependencies.items():
            # 创建该kind对应的子文件夹
            kind_folder = os.path.join(output_folder, kind)
            os.makedirs(kind_folder, exist_ok=True)

            # 输出文件路径
            output_file = os.path.join(kind_folder, "dependency_graph.json")
            print(f"Saving {kind} dependencies to: {output_file}")  # 调试输出

            # 保存该类型依赖到 JSON 文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(dep_list, f, indent=2, ensure_ascii=False)

            # 生成并保存依赖关系图
            create_dependency_plot(dep_list, kind_folder, kind)


def create_dependency_plot(dependencies, output_folder, kind):
    """根据依赖关系绘制图形"""
    # 创建图对象
    G = nx.DiGraph()

    # 添加节点和边
    for dep in dependencies:
        source = dep["source_class"] or dep["source_namespace"]
        target = dep["target_class"]
        function = dep["source_function"]
        
        G.add_node(source)
        G.add_node(target)
        G.add_edge(source, target, label=function)

    # 创建图形对象
    fig, ax = plt.subplots(figsize=(12, 8))

    # 布局
    pos = nx.spring_layout(G)

    # 绘制节点和边
    nx.draw(
        G, pos, ax=ax, with_labels=True, node_size=3000, node_color='skyblue',
        font_size=10, font_weight='bold', edge_color='gray', arrows=True
    )

    # 绘制边上的标签
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels, font_size=8)

    # 保存图像文件
    graph_image_path = os.path.join(output_folder, f"{kind}_dependency_graph.png")
    print(f"Saving {kind} graph image to: {graph_image_path}")  # 调试输出
    plt.savefig(graph_image_path, format="png")
    plt.close()


def main():
    # 设定 JSON 文件的输入目录
    input_json_dir = "ref_ana"  # 你的 JSON 文件输出目录
    output_dependency_dir = "dependency"  # 依赖图输出文件夹

    # 加载所有 JSON 文件
    json_files = load_json_files_from_directory(input_json_dir)

    # 生成每个文件夹的依赖图
    folder_dependencies = generate_dependency_graph(json_files)

    # 保存依赖图到文件夹
    save_dependency_graph(folder_dependencies, output_dependency_dir)

    print(f"Dependency graphs generated and saved to {output_dependency_dir}")


if __name__ == "__main__":
    main()
