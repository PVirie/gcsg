"""
    CYK Algorithm; polynomial time O(n^3)|G|, where |G| is the number of production rules

    Need to convert rules into the Chomsky Normal Form (CNF) first
    where A, B, and C are nonterminal symbols, the letter a is a terminal symbol (a symbol that represents a constant value), S is the start symbol, and ε denotes the empty string. Also, neither B nor C may be the start symbol, and the third production rule can only appear if ε is in L(G), the language produced by the context-free grammar G.
"""

from .utils import *


def convert_to_cnf(non_terminal_set, terminal_set, start_symbol, rules: dict):
    # CNF: Chomsky Normal Form
    # A → BC, A → a, S → ε

    new_rules = {}
    new_terminal_set = set()
    new_non_terminal_set = set()

    used_letters = set()
    used_letters.update(terminal_set)
    used_letters.update(non_terminal_set)

    # first copy all the rules
    for nt, productions in rules.items():
        new_rules[nt] = []
        for prod in productions:
            new_rules[nt].append(prod)

    # copy the terminal set
    new_terminal_set.update(terminal_set)

    # copy the non-terminal set
    new_non_terminal_set.update(non_terminal_set)

    # START 
    # Introduce a new start symbol S0, and a new rule
    new_start_symbol = get_next_free_letter(new_non_terminal_set, new_terminal_set)
    new_rules[new_start_symbol] = [start_symbol]
    new_non_terminal_set.add(new_start_symbol)

    #TERM
    new_non_terminal_set, new_terminal_set, new_start_symbol, new_rules = TERM(new_non_terminal_set, new_terminal_set, new_start_symbol, new_rules)

    #BIN
    new_non_terminal_set, new_terminal_set, new_start_symbol, new_rules = BIN(new_non_terminal_set, new_terminal_set, new_start_symbol, new_rules)

    #DEL: 
    new_non_terminal_set, new_terminal_set, new_start_symbol, new_rules = DEL(new_non_terminal_set, new_terminal_set, new_start_symbol, new_rules)

    #UNIT:
    new_non_terminal_set, new_terminal_set, new_start_symbol, new_rules = UNIT(new_non_terminal_set, new_terminal_set, new_start_symbol, new_rules)

    return new_non_terminal_set, new_terminal_set, new_start_symbol, new_rules


import numpy as np

class Context_Free_Grammar:

    def __init__(self, non_terminal_set, terminal_set, start_symbol, rules: dict):

        # first turn rules into CNF form
        non_terminal_set, terminal_set, start_symbol, rules = convert_to_cnf(non_terminal_set, terminal_set, start_symbol, rules)

        self.non_terminal_set = non_terminal_set
        self.terminal_set = terminal_set
        self.S = start_symbol
        self.rules = rules
        self.has_epsilon_rule = False
        
        # check whether has epsilon rule
        for bs in self.rules[self.S]:
            for b in bs:
                if b == "":
                    self.has_epsilon_rule = True
                    break


    def match(self, x: str) -> bool:
        # CYK Algorithm
        L = len(x)
        NT = len(self.non_terminal_set)
        nt_to_index = {nt: i for i, nt in enumerate(self.non_terminal_set)}
        # initialize the table
        table = np.zeros((L, L, NT), dtype=bool)
        # fill the table
        for i in range(L):
            for nt, productions in self.rules.items():
                for prod in productions:
                    if len(prod) == 1 and prod[0] in self.terminal_set and prod[0] == x[i]:
                        table[i, i, nt_to_index[nt]] = True
                        
        for l in range(2, L + 1):
            for i in range(L - l + 1):
                j = i + l
                for nt, productions in self.rules.items():
                    for prod in productions:
                        if len(prod) == 2:
                            A, B = prod
                            for k in range(i + 1, j):
                                if table[i, k - 1, nt_to_index[A]] and table[k, j - 1, nt_to_index[B]]:
                                    table[i, j - 1, nt_to_index[nt]] = True

        return table[0, L - 1, nt_to_index[self.S]]
    

    @staticmethod
    def check_grammar(non_terminal_set, terminal_set, start_symbol, rules: dict):
        # check whether the grammar is context free, lhs is non-terminal and a single character
        for nt, productions in rules.items():
            if len(nt) != 1 or nt not in non_terminal_set:
                return False
            for prod in productions:
                for p in prod:
                    if len(p) == 0:
                        return False
                    if p not in non_terminal_set and p not in terminal_set:
                        return False
        return True