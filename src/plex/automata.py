from functools import cmp_to_key

import networkx

from wrapper import CallWrapper


def single_edge(char: str):
    fa = Automata()
    fa.add_edge(0, 1, char)
    return fa


class Automata:
    def __init__(self):
        self.graph = networkx.MultiDiGraph()
        self.symbols: set[str] = set()
        self.accept_states: dict[int, CallWrapper] = {}
        self.start_state = 0

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
        print([(k, v('1')) for k, v in self.accept_states.items()])
        print(self.start_state)

    def execute(self, input_str: str) -> bool:
        pos = 0
        current_state: int = self.start_state
        token = ''

        def reset():
            nonlocal current_state, token
            current_state = self.start_state
            token = ''

        def find_next(state: int, char: str) -> int | None:
            for edge in self.graph[state].items():
                for label in edge[1].values():
                    if label['label'] == char:
                        return edge[0]
            return None

        deal = lambda x: print(x) if x is not None else None

        def check_and_call(state: int, token: str):
            if state in self.accept_states and token != '':
                deal(self.accept_states[state](token))
                reset()
            else:
                raise Exception("Invalid state")

        while True:
            next_state = find_next(current_state, input_str[pos])

            if next_state is None:
                check_and_call(current_state, token)
            else:
                token += input_str[pos]
                pos += 1
                current_state = next_state

            if pos == len(input_str):
                check_and_call(current_state, token)
                break

        return True
