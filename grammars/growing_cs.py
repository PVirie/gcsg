"""
    Test growing context sensitive grammar matching in polynomial time
"""

import numpy as np
from .utils import UNIT

class Growing_Context_Sensitive_Grammar:
    
    def __init__(self, non_terminal_set, terminal_set, start_symbol, rules: dict):

        non_terminal_set, terminal_set, start_symbol, rules = UNIT(non_terminal_set, terminal_set, start_symbol, rules)

        self.non_terminal_set = non_terminal_set
        self.terminal_set = terminal_set
        self.S = start_symbol
        # decompose prefix, lhs center, rhs center, and suffix for each production rule
        self.rules = {}
        for lhs, productions in rules.items():
            self.rules[lhs] = []
            # compare lhs with the rhs, prefix is the longest common prefix, suffix is the longest common suffix
            for rhs in productions:
                prefix = ""
                suffix = ""
                for i in range(min(len(lhs), len(rhs))):
                    if lhs[i] == rhs[i]:
                        prefix += lhs[i]
                    else:
                        break
                for i in range(1, min(len(lhs), len(rhs)) + 1):
                    if lhs[-i] == rhs[-i]:
                        suffix = lhs[-i] + suffix
                    else:
                        break
                self.rules[lhs].append((prefix, lhs[len(prefix):(len(lhs) - len(suffix))], rhs[len(prefix):(len(rhs) - len(suffix))], suffix))
                
        self.has_epsilon_rule = False
        for p, A, B, s in self.rules[self.S]:
            if B == "":
                self.has_epsilon_rule = True
                break


    def fit(self, vars, i, j, check_table, x):
        if len(vars) == 0:
            return True
        if i < 0 or j >= len(x) or j < i or j - i + 1 < len(vars):
            return False

        # this is regular expression matching problem, dynamic time warping
        # assume that the vars contains some non-terminal symbols, replace them in regex with *
        L = j - i + 1
        V = len(vars)
        nt_to_index = {nt: i for i, nt in enumerate(self.non_terminal_set)}
        table = np.zeros((V, L), dtype=bool)

        if vars[0] in self.non_terminal_set:
            for l in range(L):
                table[0, l] = check_table[i, i + l, nt_to_index[vars[0]]]
        else:
            table[0, 0] = vars[0] == x[i]

        for v in range(1, V):
            if vars[v] in self.non_terminal_set:
                for l in range(v, L):
                    for k in range(l):
                        if table[v - 1, k] and check_table[i + k + 1, i + l, nt_to_index[vars[v]]]:
                            table[v, l] = True
                            break
            else:
                for l in range(v, L):
                    table[v, l] = table[v - 1, l - 1] and vars[v] == x[i + l]
            
        # placeholder
        return table[V - 1, L - 1]



    def match(self, x: str) -> bool:
        # generalized CYK Algorithm
        L = len(x)
        NT = len(self.non_terminal_set)
        nt_to_index = {nt: i for i, nt in enumerate(self.non_terminal_set)}
        # initialize the table
        table = np.zeros((L, L, NT), dtype=bool)
        # fill the table
        for i in range(L):
            for lhs, productions in self.rules.items():
                for p, A, B, s in productions:
                    if B in self.terminal_set and B == x[i]:
                        # now check context, only for terminal symbols
                        x_prefix = x[max(i - len(p) + 1, 0):i]
                        x_suffix = x[i + 1:min(i + len(s) + 1, L)]
                        if (x_prefix == p or p == "") and (x_suffix == s or s == ""):
                            table[i, i, nt_to_index[A]] = True


        for l in range(2, L + 1):
            for i in range(L - l + 1):
                j = i + l
                for lhs, productions in self.rules.items():
                    for p, A, B, s in productions:
                        # check whether p can be a prefix of the substring
                        test = False
                        for k in range(i-len(p), -1, -1):
                            if self.fit(p, k, i-1, table, x):
                                test = True
                                break
                        if not test:
                            continue

                        # check whether s can be a suffix of the substring
                        test = False
                        for k in range(j + len(s) - 1, L):
                            if self.fit(s, j, k, table, x):
                                test = True
                                break
                        if not test:
                            continue

                        # now check whether the B can be the substring
                        if not self.fit(B, i, j - 1, table, x):
                            continue

                        # if all pass then make the table[i, j, nt] to be True
                        table[i, j - 1, nt_to_index[A]] = True

        return table[0, L - 1, nt_to_index[self.S]]
    

    @staticmethod
    def check_grammar(non_terminal_set, terminal_set, start_symbol, rules: dict):

        # first check context sensitive αAβ → αγβ, ignore S → *
        for nt, productions in rules.items():
            if nt == start_symbol:
                continue
            for prod in productions:
                prefix = ""
                suffix = ""
                for i in range(min(len(nt), len(prod))):
                    if nt[i] == prod[i]:
                        prefix += nt[i]
                    else:
                        break
                for i in range(1, min(len(nt), len(prod)) + 1):
                    if nt[-i] == prod[-i]:
                        suffix = nt[-i] + suffix
                    else:
                        break
                if len(prefix) + len(suffix) >= len(nt):
                    return False
                # now check whether the center is single non-terminal
                center = nt[len(prefix):(len(nt) - len(suffix))]
                if len(center) > 1 or center not in non_terminal_set:
                    return False
                
                # now check whether the grammar is non-contracting
                center_rhs = prod[len(prefix):(len(prod) - len(suffix))]
                if len(center_rhs) < len(center):
                    return False
                
                # now for growing context sensitive grammar, the center must be growing
                if len(center_rhs) <= len(center):
                    return False

        return True
