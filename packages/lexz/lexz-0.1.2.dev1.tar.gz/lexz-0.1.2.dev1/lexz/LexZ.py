from __future__ import annotations
import re
import secrets
import ast
import types
from typing import TYPE_CHECKING, Callable, Dict, List, Literal, Optional, Type
import json
import typing

if TYPE_CHECKING:
    from .alias_backend.default import AliasBackend
try:
    from dict2object import JSObject
except ModuleNotFoundError:
    import pip
    pip.main([
        'install',
        'git+https://github.com/krypton-byte/dict2object.git'
    ])
    from dict2object import JSObject

from typing import TypeVar


T = TypeVar("T")


def remove_circular_refs(ob, _seen=None):
    if _seen is None:
        _seen = set()
    if id(ob) in _seen:
        # circular reference, remove it.
        return {}
    _seen.add(id(ob))
    res = ob
    if isinstance(ob, dict):
        res = {
            remove_circular_refs(k, _seen): remove_circular_refs(v, _seen)
            for k, v in ob.items()
        }
    elif isinstance(ob, (list, tuple, set, frozenset)):
        res = type(ob)(remove_circular_refs(v, _seen) for v in ob)
    # remove id again; only *nested* references count
    _seen.remove(id(ob))
    return res


class GraphGen:
    def __init__(self, var: dict) -> None:
        self.initial = []
        self.arrow = []  # 'A->B'
        self.var = var
        self.filename = re.findall(
            r"^[a-z][a-z0-9]+", self.var["filename"], re.IGNORECASE
        )[0]

    def build_graph_string(self):
        self.gen()
        return "\n".join(
            [
                "digraph %s {" % self.filename,
                " " * 4 + ("\n" + " " * 4).join([*self.initial, *self.arrow]),
                "}",
            ]
        )

    def shape(self, annotate: Literal["Type", "Self", "Any", "Module"]):
        match annotate:
            case "Type":
                return "component"
            case "Module":
                return "note"
            case "Self":
                return "cds"
        return "hexagon"

    def gen(self, var: Optional[Dict] = None, parent: Optional[str] = None):
        r_name = "_" + secrets.token_hex(5)
        n_var = var if var else self.var
        ignore = []
        if parent:
            for node_val in n_var["vars"].values():
                if node_val['name'] not in ignore:
                    ignore.append(node_val['name'])
                    r_name = "_" + secrets.token_hex(5)
                    self.initial.append(
                        '%s [label="%s" shape="%s"]'
                        % (
                            r_name,
                            node_val['name'],
                            self.shape(node_val["annotate"])
                        )
                    )
                    self.arrow.append(f"{parent} -> {r_name}")
                    self.gen(node_val, r_name)
        else:
            self.initial.append(
                '%s [label="%s" shape="folder"]' % (r_name, n_var["filename"])
            )
            self.gen(n_var, r_name)


class VariableMapping:
    def __init__(
        self,
        filename: str,
        vars: Optional[dict] = None,
        position: Optional[List] = None,
        alias_backend: Optional[AliasBackend] = None
    ) -> None:
        self.position = position if position else []
        self.filename = filename
        self.alias_backend = alias_backend
        self.vars = (
            vars
            if vars
            else {
                "filename": self.filename,
                "vars": {},
                "annotate": "Module",
                "name": re.findall(
                    r"^[a-z][a-z0-9]+", self.filename, re.IGNORECASE
                )[0]}
        )
    
    @property
    def ismagic(self):
        if self.current()['name'].startswith('__'):
            try:
                annotate_available = self.find_variable(self.current()['annotate']).current()
            except Exception:
                annotate_available = {}
            if annotate_available and annotate_available.get('annotate') == 'Type' or self.parent().current()['annotate'] == 'Type':
                return True
        return False

    @classmethod
    def from_json_file(
        cls,
        filename: Optional[str] = None,
        parent: Optional[VariableMapping] = None
    ):
        var = cls(
            filename,
            json.load(open(filename, 'r'))
        ) if filename else parent
        if var:
            try:
                var.current()['vars'] = var.find_variable(
                    var.current()['name'])
            except Exception:
                for varname in var.current()['vars'].keys():
                    cp = var.copy()
                    cp.position.append(varname)
                    cls.from_json_file(parent=cp)
        return var

    def graph_gen(self):
        dot = GraphGen(self.Normalizer())
        return dot.build_graph_string()

    def create(
        self,
        name: str,
        alias: str,
        node: ast.AST,
        annotate: Literal["Type", "Any", "Self", "Callable"] = "Any",
    ):
        """
        creating variable
        """
        if self.position:
            data = self.vars
            for i in self.position:
                data = data["vars"][i]
            try:
                vars_data = self.find_variable(annotate).current()['vars']
            except Exception:
                vars_data = {}
            data["vars"].update(
                {
                    hex(id(node)): {
                        "alias": alias,
                        "vars": vars_data,
                        "name": name,
                        "annotate": annotate,
                        "node": {
                            "line_no": [
                                node.lineno,
                                node.end_lineno
                            ],
                            "col": [
                                node.col_offset,
                                node.end_col_offset
                            ],
                        },
                    }
                }
            )
            if self.alias_backend:
                var_cp = self.copy()
                var_cp.position.append(hex(id(node)))
                data['vars'][
                    hex(id(node))
                ]['alias'] = self.alias_backend.middleware(
                    var_cp)
        else:
            self.vars["vars"].update(
                {
                    hex(id(node)): {
                        "alias": alias,
                        "vars": {},
                        "name": name,
                        "annotate": annotate
                        }
                }
            )
            if self.alias_backend:
                var_cp = self.copy()
                var_cp.position.append(hex(id(node)))
                self.vars['vars'][hex(id(node))][
                    'alias'] = self.alias_backend.middleware(var_cp)
        return self.__class__(
            self.filename,
            self.vars,
            [*self.position, hex(id(node))],
            alias_backend=self.alias_backend
        )

    def Normalizer(self):
        """
        Remove Circular Reference
        """
        return remove_circular_refs(self.vars.copy())

    def create_class(self, name: str, alias: str, node: ast.AST):
        n = self.create(name, alias, node, annotate="Type")
        return n

    def current(self):
        data = self.vars
        for i in self.position:
            data = data["vars"][i]
        return data

    def find_variable(self, vname):
        """
        find variable from down to top
        """
        if self.position:
            stack = self.copy()
            for _ in range(self.position.__len__() + 1):
                for addr, value in stack.current()['vars'].items():
                    if value['name'] == vname:
                        stack.position.append(addr)
                        return stack
                stack = stack.parent()
        else:
            for addr, value in self.vars['vars'].items():
                if value['name'] == vname:
                    return self.__class__(
                        self.filename,
                        self.vars,
                        [addr]
                    )
        raise IndexError

    def delete(self):
        """
        Delete Variable
        """
        del self.__class__(
            self.filename, self.vars, self.position.copy()[:-1]
        ).current()[self.position[-1]]

    def to_globals(self):
        cr = self.current()
        self.vars["vars"].update({cr["name"]: cr})

    def parent(self):
        return self.jump(1)

    def jump(self, level: int):
        """
        jump to parent stack
        """
        return self.__class__(self.filename, self.vars, self.position[:-level])

    def copy(self):
        """
        copy variable with vars reference
        """
        return self.__class__(self.filename, self.vars, self.position.copy())

    def __repr__(self) -> str:
        return (
            JSObject(indent="  ").fromDict(js=self.current()).__repr__()
        )  # self.current().__str__()


class Collector:
    def __init__(self) -> None:
        self.__stmt = []
        self.__expr = []
        self.__ast = []

    def Node(
        self, ast_node: typing.Union[Type[T], types.UnionType]
    ) -> Callable[
        [Callable[[T, VariableMapping], VariableMapping]],
        Callable[[T, VariableMapping], VariableMapping],
    ]:
        def Func(f: Callable[[T, VariableMapping], VariableMapping]):
            if isinstance(ast_node, types.UnionType):
                for node_type in ast_node.__args__:
                    self.Node(node_type)(f)
            else:
                if ast.AST in ast_node.__bases__:
                    self.__ast.append((f, ast_node))
                elif ast.expr in ast_node.__bases__:
                    self.__expr.append((f, ast_node))
                elif ast.stmt in ast_node.__bases__:
                    self.__stmt.append((f, ast_node))
            return f

        return Func

    def send_node(
        self,
        node: ast.AST,
        var: VariableMapping
    ) -> VariableMapping:
        functions = []
        if ast.AST in node.__class__.__bases__:
            functions = self.__ast
        elif ast.expr in node.__class__.__bases__:
            functions = self.__expr
        elif ast.stmt in node.__class__.__bases__:
            functions = self.__stmt
        for func, ast_type in functions:
            if isinstance(node, ast_type):
                return func(node, var)
        return var
