from typing import Callable

import networkx


def single_edge(char: str):
    fa = Automata()
    fa.add_edge(0, 1, char)
    return fa


class Automata:
    def __init__(self):
        self.graph = networkx.DiGraph()
        self.symbols: set[str] = set()
        self.accept_states: dict[int, Callable] = {}

    def add_edge(self, from_node: int, to_node: int, char: str | None):
        self.graph.add_node(from_node)
        self.graph.add_node(to_node)
        self.graph.add_edge(from_node, to_node, label=char)

    def clone(self) -> 'Automata':
        new_fa = Automata()
        new_fa.graph = self.graph.copy()
        return new_fa

    def debug_print(self):
        print(self.graph)
        for node in self.graph.nodes:
            print(node, self.graph[node])
        print(self.accept_states)
