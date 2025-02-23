import os
import re
from clang.cindex import Config, Index, CursorKind, TokenKind
from collections import defaultdict
from typing import List, Tuple, Dict, Any

# 设置 Clang 库路径
libclang_path = "/usr/lib/llvm-14/lib/libclang.so"
if not os.path.exists(libclang_path):
    raise RuntimeError(f"libclang not found at {libclang_path}")
Config.set_library_file(libclang_path)

# ================== 增强控制流分析类 ==================
class EnhancedControlFlowAnalyzer:
    def __init__(self):
        self.cfg = defaultdict(list)  # 控制流图
        self.current_flow: List[Tuple[str, str]] = []  # 当前控制流上下文（类型，spelling）
        
    def enter_scope(self, cursor):
        """进入新的控制流范围，记录类型和spelling"""
        context_entry = (cursor.kind.name, cursor.spelling)
        self.current_flow.append(context_entry)
        
    def exit_scope(self):
        """退出当前控制流范围"""
        if self.current_flow:
            self.current_flow.pop()
            
    def add_relation(self, from_node, to_node):
        """添加控制流关系，使用完整上下文信息"""
        if self.current_flow:
            context = tuple(self.current_flow)
            self.cfg[context].append({
                "from": (from_node.kind.name, from_node.spelling),
                "to": (to_node.kind.name, to_node.spelling)
            })

    def get_context_string(self, context: Tuple[Tuple[str, str]]):
        """将上下文转换为可读字符串"""
        return " → ".join([f"{kind}[{spelling}]" for kind, spelling in context])

# ================== 增强数据流跟踪类 ==================
class EnhancedDataFlowTracker:
    def __init__(self):
        self.var_defs = defaultdict(list)  # 变量定义位置
        self.var_uses = defaultdict(list)  # 变量使用位置
    
    def track_variable(self, cursor):
        """跟踪变量定义和使用"""
        if cursor.kind == CursorKind.VAR_DECL:
            self.var_defs[cursor.spelling].append({
                "location": cursor.location,
                "type": cursor.type.spelling
            })
        elif cursor.kind == CursorKind.DECL_REF_EXPR:
            self.var_uses[cursor.spelling].append({
                "location": cursor.location,
                "context": cursor.get_definition().location if cursor.get_definition() else None
            })

# ================== 新版日志评分系统 ==================
class LoggingScorer:
    # 关键代码块类型及其对应分数
    CRITICAL_BLOCKS = {
        "Function Declaration": 5,
        "Method Declaration": 5,
        "Conditional Block (if)": 3,
        "Switch Block": 3,
        "Loop Block (for)": 2,
        "Loop Block (while)": 2,
        "Loop Block (do-while)": 2,
        "Return Statement": 2,
        "Error Handling Block": 4  # 示例：错误处理块
    }
    
    # 日志识别模式（仅用于存在性检查）
    LOG_PATTERNS = [
        r'\b(LBSLOG[DIWE]|TAG_LOG[DIWEF])\s*\(',
        r'\blog_(error|fatal|warn|warning|info|debug)\b',
        r'(?<!std::)cout\s*<<',
        r'\b(spdlog|glog|log4cxx)::'
    ]
    
    MISSING_PENALTY = -2  # 关键位置缺少日志的扣分

    @classmethod
    def evaluate_logging(cls, block: dict, code_block: str) -> dict:
        """基于关键位置和日志存在性的评分系统"""
        details = []
        total_score = 0
        block_type = block["type"]
        
        # 检查是否存在任何日志
        has_logging = any(
            re.search(pattern, code_block, re.IGNORECASE)
            for pattern in cls.LOG_PATTERNS
        )
        
        # 关键位置评分逻辑
        if block_type in cls.CRITICAL_BLOCKS:
            if has_logging:
                score = cls.CRITICAL_BLOCKS[block_type]
                details.append({
                    "type": f"{block_type} 日志存在",
                    "count": 1,
                    "score": score
                })
                total_score += score
            else:
                details.append({
                    "type": f"{block_type} 缺少日志",
                    "count": 1,
                    "score": cls.MISSING_PENALTY
                })
                total_score += cls.MISSING_PENALTY

        return {
            "total_score": total_score,
            "details": details,
            "has_logging": has_logging,
            "is_critical": block_type in cls.CRITICAL_BLOCKS
        }

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
    CursorKind.IF_STMT: "Conditional Block (if)",
    CursorKind.FOR_STMT: "Loop Block (for)",
    CursorKind.WHILE_STMT: "Loop Block (while)",
    CursorKind.DO_STMT: "Loop Block (do-while)",
    CursorKind.SWITCH_STMT: "Switch Block",
    CursorKind.FUNCTION_DECL: "Function Declaration",
    CursorKind.CXX_METHOD: "Method Declaration",
    CursorKind.CALL_EXPR: "Function Call",
    CursorKind.RETURN_STMT: "Return Statement",
    CursorKind.CXX_TRY_STMT: "Error Handling Block",      # 新增错误处理块
    CursorKind.CXX_CATCH_STMT: "Error Handling Block"  # 新增错误处理块
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

def extract_enhanced_blocks(cursor, source_code_file, namespace_stack=None, 
                          cf_analyzer=None, df_tracker=None, parent_block=None):
    """改进后的代码块提取"""
    if namespace_stack is None:
        namespace_stack = []
    if cf_analyzer is None:
        cf_analyzer = EnhancedControlFlowAnalyzer()
    if df_tracker is None:
        df_tracker = EnhancedDataFlowTracker()

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
                "spelling": child.spelling,
                "namespace": namespace_stack.copy(),
                "parent": parent_block,
                "complexity": calculate_complexity(child),
                "vars_defined": [],
                "vars_used": [],
                "context_chain": cf_analyzer.current_flow.copy(),
                "log_analysis": {}
            }
            
            # 建立控制流关系
            if prev_block:
                cf_analyzer.add_relation(prev_block["cursor"], child)
            prev_block = current_block
            
            blocks.append(current_block)
            
        # 递归处理子节点
        blocks.extend(extract_enhanced_blocks(child, source_code_file, namespace_stack,
                                            cf_analyzer, df_tracker, 
                                            current_block if 'current_block' in locals() else None))
        
        # 退出控制流作用域
        if child.kind in (CursorKind.IF_STMT, CursorKind.FOR_STMT,
                         CursorKind.WHILE_STMT, CursorKind.DO_STMT):
            cf_analyzer.exit_scope()
    
    # 后处理数据依赖
    for block in blocks:
        block["vars_defined"] = [v for v, locs in df_tracker.var_defs.items()
                                if any(is_in_block(loc["location"], block) for loc in locs)]
        block["vars_used"] = [v for v, locs in df_tracker.var_uses.items()
                             if any(is_in_block(loc["location"], block) for loc in locs)]
    
    return blocks

def is_in_block(location, block):
    """判断位置是否属于代码块"""
    block_start = block["cursor"].extent.start
    block_end = block["cursor"].extent.end
    return (block_start.line <= location.line <= block_end.line and
            block_start.column <= location.column <= block_end.column)

# ================== 文件解析函数 ==================
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

    if cursor.kind in [CursorKind.FUNCTION_DECL, CursorKind.CXX_METHOD]:
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

# ================== 增强分析输出 ==================
def format_context_chain(context_chain):
    """格式化上下文链"""
    return " → ".join([f"{kind}[{spelling}]" for kind, spelling in context_chain])

def analyze_cpp_file(file_path, output_ast_file, output_analysis_file):
    """解析并分析单个 C++ 文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        source_code = file.readlines()

    cursor = parse_file(file_path)

    # AST 输出
    with open(output_ast_file, 'w', encoding='utf-8') as ast_output:
        traverse_ast(cursor, ast_output)

    # 代码块分析
    blocks = extract_enhanced_blocks(cursor, file_path)
    with open(output_analysis_file, 'w', encoding='utf-8') as analysis_output:
        for block in blocks:
            block_code = extract_block_source_code(block, source_code)
            if not block_code.strip():
                continue
            
            # 执行日志分析
            log_analysis = LoggingScorer.evaluate_logging(block, block_code)
            block["log_analysis"] = log_analysis

            # 构建上下文路径
            context_path = "::".join(block["namespace"])
            if block["parent"]:
                context_path += f"::{block['parent']['type']}[{block['parent']['spelling']}]"
                
            analysis_output.write(f"代码块类型: {block['type']}\n")
            analysis_output.write(f"块名称: {block['spelling']}\n")
            analysis_output.write(f"上下文链: {format_context_chain(block['context_chain'])}\n")
            analysis_output.write(f"位置: {block['cursor'].location.file}:{block['cursor'].location.line}:{block['cursor'].location.column}\n")
            analysis_output.write(f"复杂度: {block['complexity']}\n")
            analysis_output.write(f"定义变量: {', '.join(block['vars_defined'])}\n")
            analysis_output.write(f"使用变量: {', '.join(block['vars_used'])}\n")
            analysis_output.write(f"关键位置: {'是' if log_analysis['is_critical'] else '否'}\n")
            analysis_output.write(f"日志评分: {log_analysis['total_score']}\n")
            for detail in log_analysis["details"]:
                analysis_output.write(f"  - {detail['type']}: 得分 {detail['score']}\n")
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
    analysis_output_dir = "analysis_output2"

    analyze_directory(source_dir, ast_output_dir, analysis_output_dir)
    print(f"Analysis completed. Results saved in {ast_output_dir} and {analysis_output_dir}")

if __name__ == "__main__":
    main()