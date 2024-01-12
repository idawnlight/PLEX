from typing import Callable

import nfa
from automata import Automata
from dfa import DFA, MinimalDFA
from regex import *
from wrapper import CallWrapper


class Lex:
    def __init__(self):
        self.token_specification: list[tuple[str, Callable | str]] = []

        self._table = {}

        self.automata: Automata | None = None

    def _init(self):
        # parse token specifications
        fas: list[Automata] = []
        print(f"[+] From {len(self.token_specification)} token specifications (RegExp) to NFAs...")
        for idx, rule in enumerate(self.token_specification):
            reg = RegexExpr(rule[0])
            # print(reg.get_regex_chars())
            fas.append(nfa.from_regex_string(reg, CallWrapper(rule[1], idx)))
            # print(rule[0])
            # fas[-1].debug_print()
        print("[+] Combining NFAs to a single one...")
        combined_nfa = nfa.combine(fas)
        # combined_nfa.debug_print()
        print("[+] From combined NFA to DFA...")
        dfa = DFA(combined_nfa)
        # dfa.result.debug_print()
        # for i in dfa.result.accept_states:
        #     print(i, dfa.result.accept_states[i](1))

        print("[+] From DFA to minimal DFA...")
        minimal_dfa = MinimalDFA(dfa.result)
        # minimal_dfa.result.debug_print()

        self.automata = minimal_dfa.result

    def tokenize(self, source_code: str):
        print("[+] Executing minimal DFA...")
        self.automata.execute(source_code)
