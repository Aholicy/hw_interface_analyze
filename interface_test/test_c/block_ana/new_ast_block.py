import os
import re
from clang.cindex import Config, Index, CursorKind, TokenKind
from collections import defaultdict

# 设置 Clang 库路径
libclang_path = "/usr/lib/llvm-14/lib/libclang.so"
if not os.path.exists(libclang_path):
    raise RuntimeError(f"libclang not found at {libclang_path}")
Config.set_library_file(libclang_path)

# ================== 新增分析类 ==================
class ControlFlowAnalyzer:
    def __init__(self):
        self.cfg = defaultdict(list)  # 控制流图
        self.current_flow = []        # 当前控制流上下文
        
    def enter_scope(self, cursor):
        """进入新的控制流范围"""
        self.current_flow.append(cursor.hash)
        
    def exit_scope(self):
        """退出当前控制流范围"""
        if self.current_flow:
            self.current_flow.pop()
            
    def add_relation(self, from_node, to_node):
        """添加控制流关系"""
        if self.current_flow:
            context = tuple(self.current_flow)
            self.cfg[context].append((from_node, to_node))

class DataFlowTracker:
    def __init__(self):
        self.var_defs = defaultdict(list)  # 变量定义位置
        self.var_uses = defaultdict(list)  # 变量使用位置
    
    def track_variable(self, cursor):
        """跟踪变量定义和使用"""
        if cursor.kind == CursorKind.VAR_DECL:
            self.var_defs[cursor.spelling].append(cursor.location)
        elif cursor.kind == CursorKind.DECL_REF_EXPR:
            self.var_uses[cursor.spelling].append(cursor.location)

# ================== AST遍历函数 ==================
def traverse_ast(cursor, output_file, level=0):
    """递归遍历 AST 并输出每个节点的详细信息"""
    indent = " " * (level * 2)
    cursor_info = f"{indent}Cursor Kind: {cursor.kind} | Spelling: {cursor.spelling} | Location: {cursor.location.file}:{cursor.location.line}:{cursor.location.column}"
    output_file.write(cursor_info + "\n")

    for child in cursor.get_children():
        traverse_ast(child, output_file, level + 1)

def is_in_source_file(cursor, source_code_file):
    """检查 AST 节点是否属于源文件"""
    location = cursor.location
    if not location.file:
        return False
    return os.path.samefile(location.file.name, source_code_file)

# ================== 增强代码块分析 ==================
EXTENDED_BLOCK_TYPES = {
    # 控制流相关
    CursorKind.BREAK_STMT: "Break Statement",
    CursorKind.CONTINUE_STMT: "Continue Statement",
    CursorKind.CASE_STMT: "Case Statement",
    CursorKind.DEFAULT_STMT: "Default Statement",
    CursorKind.IF_STMT: "Conditional Block (if)",
    CursorKind.FOR_STMT: "Loop Block (for)",
    CursorKind.WHILE_STMT: "Loop Block (while)",
    CursorKind.DO_STMT: "Loop Block (do-while)",
    CursorKind.SWITCH_STMT: "Switch Block",
    
    # 函数相关
    CursorKind.FUNCTION_DECL: "Function Declaration",
    CursorKind.CXX_METHOD: "Method Declaration",
    CursorKind.CALL_EXPR: "Function Call",
    CursorKind.RETURN_STMT: "Return Statement",
    CursorKind.CONSTRUCTOR: "Constructor Declaration",
    CursorKind.DESTRUCTOR: "Destructor Declaration",
    
    # 面向对象
    CursorKind.CLASS_DECL: "Class Declaration",
    CursorKind.ENUM_DECL: "Enum Declaration",
    CursorKind.FIELD_DECL: "Class Field",
    CursorKind.CXX_BASE_SPECIFIER: "Base Class Specifier",
    
    # 变量操作
    CursorKind.VAR_DECL: "Variable Declaration",
    CursorKind.DECL_STMT: "Declaration Statement",
    CursorKind.DECL_REF_EXPR: "Variable Reference",
    
    # 异常处理
    CursorKind.CXX_TRY_STMT: "Exception Handling Block (try)",
    CursorKind.CXX_CATCH_STMT: "Exception Handling Block (catch)",

    
    # 其他
    CursorKind.NAMESPACE: "Namespace Declaration",
    CursorKind.TEMPLATE_REF: "Template Reference",
    CursorKind.TYPEDEF_DECL: "Type Alias",
    CursorKind.BINARY_OPERATOR: "Binary Operation",
    CursorKind.UNARY_OPERATOR: "Unary Operation",
    CursorKind.LAMBDA_EXPR: "Lambda Expression"
}

def get_block_type(cursor):
    """扩展后的代码块类型判断"""
    return EXTENDED_BLOCK_TYPES.get(cursor.kind, "Other Block")

def calculate_complexity(cursor):
    """计算代码块复杂度"""
    complexity = 0
    for token in cursor.get_tokens():
        if token.kind == TokenKind.KEYWORD and token.spelling in ['if', 'else', 'case', 'for', 'while', '&&', '||', '?']:
            complexity += 1
    return complexity

def extract_blocks(cursor, source_code_file, namespace_stack=None, 
                  cf_analyzer=None, df_tracker=None, parent_block=None):
    """改进后的代码块提取"""
    if namespace_stack is None:
        namespace_stack = []
    if cf_analyzer is None:
        cf_analyzer = ControlFlowAnalyzer()
    if df_tracker is None:
        df_tracker = DataFlowTracker()

    blocks = []
    prev_block = None
    
    for child in cursor.get_children():
        df_tracker.track_variable(child)
        
        # 处理控制流作用域
        if child.kind in (CursorKind.IF_STMT, CursorKind.FOR_STMT, 
                         CursorKind.WHILE_STMT, CursorKind.DO_STMT):
            cf_analyzer.enter_scope(child)
            
        # 提取代码块
        block_type = get_block_type(child)
        if block_type != "Other Block" and is_in_source_file(child, source_code_file):
            current_block = {
                "type": block_type,
                "cursor": child,
                "namespace": namespace_stack.copy(),
                "parent": parent_block,
                "complexity": calculate_complexity(child),
                "vars_defined": [],
                "vars_used": []
            }
            
            # 建立控制流关系
            if prev_block:
                cf_analyzer.add_relation(prev_block["cursor"].hash, child.hash)
            prev_block = current_block
            
            blocks.append(current_block)
            
        # 递归处理子节点
        blocks.extend(extract_blocks(child, source_code_file, namespace_stack,
                                    cf_analyzer, df_tracker, current_block if 'current_block' in locals() else None))
        
        # 退出控制流作用域
        if child.kind in (CursorKind.IF_STMT, CursorKind.FOR_STMT,
                         CursorKind.WHILE_STMT, CursorKind.DO_STMT):
            cf_analyzer.exit_scope()
    
    # 后处理数据依赖
    for block in blocks:
        block["vars_defined"] = [v for v, locs in df_tracker.var_defs.items()
                                if any(is_in_block(loc, block) for loc in locs)]
        block["vars_used"] = [v for v, locs in df_tracker.var_uses.items()
                             if any(is_in_block(loc, block) for loc in locs)]
    
    return blocks

def is_in_block(location, block):
    """判断位置是否属于代码块"""
    block_start = block["cursor"].extent.start
    block_end = block["cursor"].extent.end
    return (block_start.line <= location.line <= block_end.line and
            block_start.column <= location.column <= block_end.column)

# ================== 原有解析函数 ==================
def parse_file(file_path):
    """解析 C++ 文件并返回 AST 根节点"""
    index = Index.create()
    standard_lib_path = "/usr/lib/llvm-14/lib/clang/14.0.0"  
    args = [
        '-std=c++17',
        '-stdlib=libc++',
        f'-I{standard_lib_path}',
        '-I/usr/include/c++/12',
        '-I/usr/include/x86_64-linux-gnu/c++/12/',
        # '-L/usr/lib/gcc/x86_64-linux-gnu/7',
        '-Dsize_t=unsigned long',  # 添加占位符定义
        '-ferror-limit=1000', # 允许错误限制
    ]
    
    include_dirs_file = 'include_dirs.txt'
    if os.path.exists(include_dirs_file):
        with open(include_dirs_file, 'r') as f:
            include_dirs = f.readlines()
            args.extend(line.strip() for line in include_dirs)
            
    tu = index.parse(file_path, args=args)
    if not tu:
        raise Exception(f"Failed to parse file: {file_path}")
    if tu.diagnostics:
        for diag in tu.diagnostics:
            print(f"Diagnostic: {diag.spelling} in {diag.location.file}:{diag.location.line}:{diag.location.column}")
    return tu.cursor

def get_complete_block(cursor):
    """获取完整的代码块范围"""
    start = cursor.extent.start
    end = cursor.extent.end

    if cursor.kind in [CursorKind.FUNCTION_DECL, CursorKind.CXX_METHOD, 
                      CursorKind.CONSTRUCTOR, CursorKind.DESTRUCTOR]:
        for child in cursor.get_children():
            if child.kind == CursorKind.COMPOUND_STMT:
                end = child.extent.end
                break

    return start, end

def extract_block_source_code(block, source_code):
    """提取完整的代码块源代码"""
    start, end = get_complete_block(block["cursor"])
    start_line = max(0, start.line - 1)
    end_line = min(len(source_code), end.line)
    return ''.join(source_code[start_line:end_line])

# ================== 增强日志检测 ==================
def contains_logging_statement(code_block):
    """改进的日志语句检测"""
    patterns = [
        r'\b(LBSLOG[DIWE]|TAG_LOG[DIWEF])\s*\(',
        r'(?<!std::)cout\s*<<',
        r'\blog_(debug|info|warning|error)\b',
        r'\b(spdlog|glog|log4cxx)::',
        r'(fprintf|syslog)\s*\(.*?(\b(stderr|LOG_\w+))'
    ]
    return any(re.search(p, code_block, re.IGNORECASE) for p in patterns)

# ================== 分析输出函数 ==================
def analyze_cpp_file(file_path, output_ast_file, output_analysis_file):
    """解析并分析单个 C++ 文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        source_code = file.readlines()

    cursor = parse_file(file_path)

    # AST 输出
    with open(output_ast_file, 'w', encoding='utf-8') as ast_output:
        traverse_ast(cursor, ast_output)

    # 代码块分析
    blocks = extract_blocks(cursor, file_path)
    with open(output_analysis_file, 'w', encoding='utf-8') as analysis_output:
        for block in blocks:
            block_code = extract_block_source_code(block, source_code)
            if not block_code.strip():
                continue
            
            context_path = "::".join(block["namespace"])
            if block["parent"]:
                context_path += f"::{block['parent']['type']}"
                
            analysis_output.write(f"代码块类型: {block['type']}\n")
            analysis_output.write(f"上下文: {context_path}\n")
            analysis_output.write(f"位置: {block['cursor'].location.file}:{block['cursor'].location.line}:{block['cursor'].location.column}\n")
            analysis_output.write(f"复杂度: {block['complexity']}\n")
            analysis_output.write(f"定义变量: {', '.join(block['vars_defined'])}\n")
            analysis_output.write(f"使用变量: {', '.join(block['vars_used'])}\n")
            analysis_output.write(f"包含日志: {'是' if contains_logging_statement(block_code) else '否'}\n")
            analysis_output.write(f"代码:\n{block_code}\n")
            analysis_output.write("-"*80 + "\n")

def analyze_directory(directory_path, output_ast_dir, output_analysis_dir):
    """分析目录中的所有 C++ 文件"""
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".cpp"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, directory_path)

                ast_output_subdir = os.path.join(output_ast_dir, relative_path)
                analysis_output_subdir = os.path.join(output_analysis_dir, relative_path)

                os.makedirs(ast_output_subdir, exist_ok=True)
                os.makedirs(analysis_output_subdir, exist_ok=True)

                output_ast_file = os.path.join(ast_output_subdir, f"{file}_ast.txt")
                output_analysis_file = os.path.join(analysis_output_subdir, f"{file}_analysis.txt")

                analyze_cpp_file(file_path, output_ast_file, output_analysis_file)

def main():
    """主函数"""
    source_dir = "/home/user/yzb/hw_interface_analyze/interface_test/test_c/ability_ability_runtime/interfaces/inner_api"
    ast_output_dir = "ast_output"
    analysis_output_dir = "analysis_output"

    analyze_directory(source_dir, ast_output_dir, analysis_output_dir)
    print(f"Analysis completed. Results saved in {ast_output_dir} and {analysis_output_dir}")

if __name__ == "__main__":
    main()