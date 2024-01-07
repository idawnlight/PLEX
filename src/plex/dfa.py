from dataclasses import dataclass
from typing import Callable

from automata import Automata


class DFA:
    @dataclass
    class DFAState:
        id: int
        states: set[int]
        action: Callable | None

        def __init__(self, _id: int, states: set[int], action: Callable | None):
            self.id = _id
            self.states = states
            self.action = action

    def __init__(self, nfa: Automata):
        self.nfa = nfa

        dfa_states: list[DFA.DFAState] = []
        transition_table: list[dict[str, int | None]] = []
        current_row = 0

        print("start closure", self.nfa_epsilon_closure(0))
        start_closure = self.nfa_epsilon_closure(0)
        dfa_states.append(DFA.DFAState(current_row, start_closure, self.get_action(start_closure)))

        while current_row < len(dfa_states):
            transition_table.append(self.empty_table_entry())
            for symbol in self.nfa.symbols:
                char_closure = set()
                for state in dfa_states[current_row].states:
                    char_closure = char_closure.union(self.nfa_char_closure(state, symbol))
                # print("current row", current_row, "from", dfa_states[current_row].states, "symbol", symbol, "char closure", char_closure)
                if len(char_closure) > 0:
                    # check if this state is already in dfa_states
                    found = False
                    for state in dfa_states:
                        if state.states == char_closure:
                            transition_table[current_row][symbol] = state.id
                            found = True
                            break
                    if not found:
                        dfa_states.append(DFA.DFAState(len(dfa_states), char_closure, self.get_action(char_closure)))
                        transition_table[current_row][symbol] = len(dfa_states) - 1
            current_row += 1

        # print("transition table", transition_table)
        self.result = Automata()
        self.result.symbols = self.nfa.symbols
        for i in range(len(transition_table)):
            for symbol in self.result.symbols:
                if transition_table[i][symbol] is not None:
                    self.result.add_edge(i, transition_table[i][symbol], symbol)
                    # print(self.result.graph)

        for state in dfa_states:
            if state.action is not None:
                self.result.accept_states[state.id] = state.action

        # print(dfa_states)

    def empty_table_entry(self) -> dict[str, None]:
        return dict([(c, None) for c in self.nfa.symbols])

    # find all states that can be reached from start state with epsilon (None) edges
    def nfa_epsilon_closure(self, start: int) -> set[int]:
        result: set[int] = set()
        queue: list[int] = [start]
        visited: set[int] = set()
        while len(queue) > 0:
            cur = queue.pop()
            result.add(cur)
            visited.add(cur)
            for edge in self.nfa.graph[cur].items():
                if edge[1]['label'] is None and edge[0] not in visited:
                    queue.append(edge[0])
        return result

    # find all states that can be reached from start state with char edges (and epsilon edges)
    def nfa_char_closure(self, start: int, char: str) -> set[int]:
        char_result: set[int] = set()
        for edge in self.nfa.graph[start].items():
            if edge[1]['label'] == char:
                char_result.add(edge[0])

        result = set()
        for state in char_result:
            result = result.union(self.nfa_epsilon_closure(state))
        return result

    def get_action(self, nfa_states: set[int]) -> Callable | None:
        for state in nfa_states:
            if state in self.nfa.accept_states:
                return self.nfa.accept_states[state]
        return None
