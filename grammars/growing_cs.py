"""
    Test growing context sensitive grammar matching in polynomial time
"""

import numpy as np


class Growing_Context_Sensitive_Grammar:
    
    def __init__(self, non_terminal_set, terminal_set, start_symbol, rules: dict):
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

        def can_be(vars, i, j, table, x):
            if len(vars) == 0:
                return True

            # if var starts or end with terminal symbol use that to filter
            for p in range(len(vars)):
                if vars[p] in self.terminal_set: 
                    if vars[p] != x[i + p]:
                        return False
                else:
                    break

            for p in range(len(vars) - 1, -1, -1):
                if vars[p] in self.terminal_set:
                    if vars[p] != x[j - len(vars) + 1 + p]:
                        return False
                else:
                    break

            # now attempt to align the substring while matching the non-terminal
            # for example AaaCbbB can be matched with aabb,  aaabbb

            # placeholder
            return True

        for l in range(2, L + 1):
            for i in range(L - l + 1):
                j = i + l
                for lhs, productions in self.rules.items():
                    for p, A, B, s in productions:
                        # check whether p can be a prefix of the substring
                        test = False
                        for k in range(i-len(p), -1, -1):
                            if can_be(p, k, i-1, table, x):
                                test = True
                                break
                        if not test:
                            continue

                        # check whether s can be a suffix of the substring
                        test = False
                        for k in range(j + len(s) - 1, L):
                            if can_be(s, j, k, table, x):
                                test = True
                                break
                        if not test:
                            continue

                        # now check whether the B can be the substring
                        if not can_be(B, i, j - 1, table, x):
                            continue

                        # if all pass then make the table[i, j, nt] to be True
                        table[i, j - 1, nt_to_index[A]] = True

        return table[0, L - 1, nt_to_index[self.S]]
    

    @staticmethod
    def check_grammar(non_terminal_set, terminal_set, start_symbol, rules: dict):

        # first check context sensitive αAβ → αγβ
        for nt, productions in rules.items():
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
