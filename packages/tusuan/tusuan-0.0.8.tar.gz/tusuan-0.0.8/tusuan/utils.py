import ast
import inspect

import astunparse


# 定义一个自定义的访问者类，继承自ast.NodeVisitor
class ForLoopVisitor(ast.NodeVisitor):
    def visit_For(self, node):
        if isinstance(node.iter, ast.Name):
            iter_name = node.iter.id
            # print("For loop variable:", iter_name)
            self.iter_name = iter_name

        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            # print("For loop variable:", var_name)
            self.var_name = var_name

        # 继续遍历子节点
        self.generic_visit(node)


def extract_block_codes():
    frame = inspect.currentframe().f_back.f_back
    code_obj = frame.f_code
    file_name = code_obj.co_filename
    current_line = frame.f_lineno

    # print(current_line)
    # print("file_name", file_name)
    # print("current_line", current_line)
    with open(file_name, 'r') as file:
        code = file.read()

    ast_tree = ast.parse(code)
    # print(ast_tree.body)

    possible_nodes = []
    for node in ast.walk(ast_tree):
        # if isinstance(node, ast.With) and node.lineno <= current_line <= node.body[-1].lineno:
        if isinstance(node, ast.If) and node.lineno <= current_line <= node.end_lineno:
            # print("Found function definition:", node.lineno, node.end_lineno, node)
            possible_nodes.append((node.end_lineno - node.lineno, node))
    return min(possible_nodes, key=lambda x: x[0])[1]


def for_to_multiprocess(g, l):
    # print("Entering context")
    try:
        block_codes = extract_block_codes().body

        print(astunparse.unparse(block_codes))

        # 创建访问者对象并遍历AST
        visitor = ForLoopVisitor()
        visitor.visit(block_codes[0])
        print(visitor.var_name, visitor.iter_name)

        process_item_def = ast.FunctionDef(
                name='process_item',
                args=ast.arguments(args=[ast.arg(arg=visitor.var_name, annotation=None)],
                                   vararg=None, kwonlyargs=[],
                                   kw_defaults=[], kwarg=None, defaults=[]),
                body=[*block_codes[0].body,
                      ast.Return(value=ast.Name(id='result', ctx=ast.Load()))],
                decorator_list=[],
                # returns=return_annotation
        )

        multiprocessing_codes = f"""
from concurrent.futures import ThreadPoolExecutor

items = {visitor.iter_name}
with ThreadPoolExecutor() as executor:
    RESULTS = executor.map(process_item, {visitor.iter_name})
        """

        # exec(astunparse.unparse(function_def), self.g, self.l)
        exec(astunparse.unparse(process_item_def), g, l)
        exec(multiprocessing_codes, g, l)
        g["RESULTS"] = l.get("RESULTS", None)

        return False
    finally:
        print("Exiting context")  # 这里的代码相当于__exit__方法
