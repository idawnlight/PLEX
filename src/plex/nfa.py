from typing import Callable

from regex import RegexExpr
import automata
from automata import Automata


def combine(fas: list[Automata]) -> Automata:
    new_fa = Automata()

    offset = 1
    for fa in fas:
        for edge in fa.graph.edges.items():
            new_fa.add_edge(edge[0][0] + offset, edge[0][1] + offset, edge[1]['label'])
        new_fa.add_edge(0, offset, None)
        new_fa.symbols = new_fa.symbols.union(fa.symbols)
        for k, v in fa.accept_states.items():
            new_fa.accept_states[k + offset] = v

        offset += fa.graph.number_of_nodes()

    return new_fa


def concat(fa1: Automata, fa2: Automata) -> Automata:
    new_fa = fa1.clone()

    offset = len(new_fa.graph.nodes) - 1
    for edge in fa2.graph.edges.items():
        new_fa.add_edge(edge[0][0] + offset, edge[0][1] + offset, edge[1]['label'])

    return new_fa


def union(fa1: Automata, fa2: Automata) -> Automata:
    new_fa = Automata()
    # New end node: fa1.graph.number_of_nodes() + fa2.graph.number_of_nodes() + 1
    end_node = fa1.graph.number_of_nodes() + fa2.graph.number_of_nodes() + 1

    offset = 1
    new_fa.add_edge(0, offset, None)
    for edge in fa1.graph.edges.items():
        new_fa.add_edge(edge[0][0] + offset, edge[0][1] + offset, edge[1]['label'])
    new_fa.add_edge(fa1.graph.number_of_nodes() + offset - 1, end_node, None)

    offset = offset + fa1.graph.number_of_nodes()
    new_fa.add_edge(0, offset, None)
    for edge in fa2.graph.edges.items():
        new_fa.add_edge(edge[0][0] + offset, edge[0][1] + offset, edge[1]['label'])
    new_fa.add_edge(fa2.graph.number_of_nodes() + offset - 1, end_node, None)

    return new_fa


def kleene_closure(fa: Automata) -> Automata:
    new_fa = Automata()
    # Three additional nodes
    # 1. New start node 0, connect to intermediate node with epsilon edge
    # 2. New end node fa.graph.number_of_nodes() + 2, intermediate node connects to this node with epsilon edge
    # 3. Intermediate node 1 that connects to old start node with epsilon edge, and old end node with epsilon edge
    new_fa.add_edge(0, 1, None)
    new_fa.add_edge(1, 2, None)

    offset = 2
    for edge in fa.graph.edges.items():
        new_fa.add_edge(edge[0][0] + offset, edge[0][1] + offset, edge[1]['label'])

    new_fa.add_edge(fa.graph.number_of_nodes() + offset - 1, 1, None)
    new_fa.add_edge(1, fa.graph.number_of_nodes() + offset, None)

    return new_fa


def from_regex_string(regexpr: RegexExpr, action: Callable) -> Automata:
    stk: list[Automata] = []
    for c in regexpr.get_regex_chars():
        if not c.is_operator:
            stk.append(automata.single_edge(c.char))
        else:
            if c.char == '@':
                second = stk.pop()
                first = stk.pop()
                stk.append(concat(first, second))
            elif c.char == '|':
                stk.append(union(stk.pop(), stk.pop()))
            elif c.char == '*':
                stk.append(kleene_closure(stk.pop()))

    result = stk.pop()
    result.symbols = set([c.char for c in regexpr.get_regex_chars() if not c.is_operator])
    result.accept_states = {result.graph.number_of_nodes() - 1: action}

    return result
