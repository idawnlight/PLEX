from typing import Callable

from regex import *
import nfa
from automata import Automata
from dfa import DFA


def call_wrapper(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    if callable(func):
        return wrapper
    else:
        return lambda _: func


class Lex:
    def __init__(self):
        self.token_specification: list[tuple[str, Callable | str]] = []

        self._table = {}

    def _tokenize(self, source_code: str):
        # parse token specifications
        fas: list[Automata] = []
        print("[+] From token specifications (RegExp) to NFAs...")
        for rule in self.token_specification:
            reg = RegexExpr(rule[0])
            # print(reg.get_regex_chars())
            fas.append(nfa.from_regex_string(reg, call_wrapper(rule[1])))
            # print(rule[0])
            # fas[-1].debug_print()
        print("[+] Combining NFAs to a single one...")
        combined_nfa = nfa.combine(fas)
        # combined_nfa.debug_print()
        print("[+] From combined NFA to DFA...")
        dfa = DFA(combined_nfa)
        dfa.result.debug_print()
        for i in dfa.result.accept_states:
            print(i, dfa.result.accept_states[i](1))
