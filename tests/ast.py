from typing import Callable, Optional, Any, List, Type
from pathlib import Path
import ast
from ast import AST, FunctionDef, NodeVisitor, AsyncFunctionDef, Call, Name, Constant, Attribute


class Ast(NodeVisitor):
    def __init__(self, filename: Path) -> None:
        content = filename.read_text()
        self._tree = ast.parse(content)
        self._names: list[str] = list()
        self._constants: list[str] = list()
        self._attrs: list[str] = list()
        self._call_args: list[str] = list()

    def get_visit(self) -> None:
        self.visit(self._tree)

    def visit_node(self, node: AST) -> AST:
        self.visit(node)

    def get_AsyncFunctionDef(self, name: str) -> Optional[AsyncFunctionDef]:
        for node in ast.walk(self._tree):
            if (
                isinstance(node, AsyncFunctionDef) and
                node.name == name
            ):
                return node

    def visit_Name(self, node: Name) -> None:
        self._names.append(node.id)
        self.generic_visit(node)

    def visit_Constant(self, node: Constant) -> None:
        self._constants.append(node.value)
        self.generic_visit(node)

    def visit_Attribute(self, node: Attribute) -> None:
        self._attrs.append(node.attr)
        self.generic_visit(node)

    def visit_Call(self, node: Call) -> None:
        for keyword in node.keywords:
            self._call_args.append(keyword.arg)
        self.generic_visit(node)
