import clang.cindex
import networkx as nx

# 初始化libclang
clang.cindex.Config.set_library_file("/usr/lib/llvm-14/lib/libclang.so")  

# 解析类的依赖关系
def extract_dependencies(filename):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(filename, args=["-lstdc++ -std=c++17 -I/home/user/yzb/hw_interface_analyze/interface_test/test_c/ability_ability_runtime/interfaces/inner_api/ability_manager/include"])
    
    dependencies = {}

    def visit(node, current_class=None):
        print(node.spelling)
        if node.kind == clang.cindex.CursorKind.CLASS_DECL and node.is_definition():
            # 当前类的名字
            class_name = node.spelling
            dependencies[class_name] = set()
            current_class = class_name

        # 查找基类
        if node.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
            if current_class:
                dependencies[current_class].add(node.spelling)
                print(f"{current_class} -> {node.spelling}")

        # 查找成员变量类型和函数参数类型
        if node.kind in (clang.cindex.CursorKind.FIELD_DECL, clang.cindex.CursorKind.PARM_DECL):
            if current_class:
                type_name = node.type.spelling.split("::")[-1]
                dependencies[current_class].add(type_name)
                print(f'{current_class} -> {type_name}')

        for child in node.get_children():
            visit(child, current_class)

    def print_ast(node, depth=0):
        loc = f"{node.location.file}:{node.location.line}" if node.location.file else "unknown"
        extent = f"{node.extent.start.line}-{node.extent.end.line}" if node.extent.start else "unknown"
        print(f"{'  ' * depth}{node.kind}: {node.spelling} ({loc}, {extent})")
        for child in node.get_children():
            # print(child.spelling)
            print_ast(child, depth + 1)

    # visit(translation_unit.cursor)
    print_ast(translation_unit.cursor)
    return dependencies

# 构建依赖图并可视化
def build_dependency_graph(dependencies):
    graph = nx.DiGraph()
    for cls, deps in dependencies.items():
        for dep in deps:
            graph.add_edge(cls, dep)
    return graph

# 主函数
if __name__ == "__main__":
    filename = "./main.cpp"  # 替换为你的 .h 文件路径
    dependencies = extract_dependencies(filename)
    
    # 打印依赖关系
    for cls, deps in dependencies.items():
        print(f"Class {cls} depends on: {', '.join(deps) if deps else 'None'}")

    # # 构建依赖图
    # dependency_graph = build_dependency_graph(dependencies)

    # # 保存图为图片
    # nx.draw(dependency_graph, with_labels=True, node_color='lightblue', font_size=10, node_size=2000)
    # import matplotlib.pyplot as plt
    # plt.savefig("dependency_graph.png")
    # plt.show()