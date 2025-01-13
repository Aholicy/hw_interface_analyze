import json
import networkx as nx
import matplotlib.pyplot as plt

def build_dependency_graph(parsed_data):
    """构建依赖图"""
    G_inheritance = nx.DiGraph()  # 用于继承关系的图
    G_params = nx.DiGraph()  # 用于参数依赖的图

    # 遍历所有模块，提取依赖关系
    for module_name, data in parsed_data.items():
        # 添加模块名作为图的一个节点
        G_inheritance.add_node(module_name)
        G_params.add_node(module_name)

        for class_name, class_data in data['classes'].items():
            # 获取继承信息
            inheritance = class_data.get('dependencies', {}).get('inheritance', {})
            if inheritance:
                current_class = inheritance.get('class')  # 获取当前类名
                base_class = inheritance.get('base_class')  # 获取基类名
                base_class_module = inheritance.get('base_class_module')  # 获取基类模块

                # 如果base_class_module为None，设置为base_class
                if base_class_module is None:
                    base_class_module = base_class
                    G_inheritance.add_node(base_class)  # 确保基类模块作为节点存在
                
                # 添加继承关系依赖边
                G_inheritance.add_edge(module_name, base_class_module, label='inherits from')
                print(module_name+" inherits from "+base_class_module)
            # 方法参数依赖
            for method_name, method_dependencies in class_data['dependencies']['parameters'].items():
                # 处理global依赖
                for param_type in method_dependencies['global']:
                    # 直接从global中获取模块依赖
                    depenent_module = method_dependencies['global'][param_type]
                    G_params.add_edge(module_name, depenent_module, label=f'param dependency for {method_name}')
                    print(f'param dependency for {method_name} from {module_name} to {depenent_module}')

    return G_inheritance, G_params

def draw_dependency_graph(G, title, filename):
    """绘制依赖图"""
    nodes_with_edges = [node for node in G.nodes() if G.out_degree(node) > 0 or G.in_degree(node) > 0]

    # 从图中提取这些节点
    G_subgraph = G.subgraph(nodes_with_edges)

    pos = nx.spring_layout(G_subgraph, seed=42)  # 固定随机种子，确保图形布局一致
    plt.figure(figsize=(14, 14))  # 图的大小

    # 节点的标签和边的标签
    labels = {node: node for node in G_subgraph.nodes()}
    edge_labels = nx.get_edge_attributes(G_subgraph, 'label')

    # 根据边的类型来设置边的颜色
    edge_colors = ['blue' if label == 'inherits from' else 
                   ('green' if 'param dependency' in label else 'red')
                   for _, _, label in G_subgraph.edges(data='label')]

    nx.draw_networkx_nodes(G_subgraph, pos, node_size=500, node_color='lightblue')
    nx.draw_networkx_edges(G_subgraph, pos, edge_color=edge_colors, width=2)
    nx.draw_networkx_labels(G_subgraph, pos, labels, font_size=10, font_weight='bold')

    # 添加边的标签
    nx.draw_networkx_edge_labels(G_subgraph, pos, edge_labels=edge_labels)

    # 设置标题并显示
    plt.title(title)
    plt.axis('off')  # 不显示坐标轴
    plt.tight_layout()  # 自动调整布局，防止标签重叠
    plt.savefig(filename)  # 保存图形
    plt.show()  # 显示图形

def main():
    parsed_file = "enhanced_parsed_interfaces2.json"  # 输入解析后的 JSON 文件
    # 加载解析后的数据
    with open(parsed_file, 'r', encoding='utf-8') as file:
        parsed_data = json.load(file)
    
    # 构建依赖图
    G_inheritance, G_params = build_dependency_graph(parsed_data)
    
    # 绘制继承关系子图
    draw_dependency_graph(G_inheritance, "Module Inheritance Dependency Graph", "inheritance_dependency_graph.png")
    
    # 绘制参数依赖子图
    draw_dependency_graph(G_params, "Module Parameter Dependency Graph", "parameter_dependency_graph.png")

if __name__ == "__main__":
    main()
