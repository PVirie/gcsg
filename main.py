"""
    Test growing context sensitive grammar matching in polynomial time
"""

import numpy as np


class Recursive_Grammar:

    def __init__(self, non_terminal_set, terminal_set, start_symbol, rules: dict):
        self.non_terminal_set = non_terminal_set
        self.terminal_set = terminal_set
        self.S = start_symbol
        self.rules = rules

        self._reverse_rules = {}
        for nt, productions in rules.items():
            for prod in productions:
                self._reverse_rules[prod] = nt

    def match(self, x: str, cache=None) -> bool:
        # recursively
        if cache is None:
            cache = {self.S: True}

        if x in cache:
            return cache[x]
        
        for i in range(1, len(x) + 1):
            for j in range(0, i):
                substr = x[j:i]
                # n
                replacement = self._reverse_rules.get(substr)
                if replacement:
                    if self.match(x[:j] + replacement + x[i:], cache):
                        cache[x] = True
                        return True
        cache[x] = False
        return False
    

    @staticmethod
    def check_grammar(rules: dict):
        return True


class Growing_Context_Sensitive_Grammar:
    
    def __init__(self, non_terminal_set, terminal_set, start_symbol, rules: dict):
        self.non_terminal_set = non_terminal_set
        self.terminal_set = terminal_set
        self.S = start_symbol
        # decompose prefix, change, and suffix for each production rule
        self.rules = {}
        for nt, productions in rules.items():
            self.rules[nt] = []
            # compare nt with the outcome, prefix is the longest common prefix, suffix is the longest common suffix
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
                self.rules[nt].append((prefix, prod[len(prefix):(len(prod) - len(suffix))], suffix))


    def match(self, x: str, cache=None) -> bool:
        pass

    @staticmethod
    def check_grammar(rules: dict):
        for nt, productions in rules.items():
            for prod in productions:
                if len(prod) < len(nt):
                    return False
        return True



def build_grammar(non_terminal_set, terminal_set, start_symbol, rules):
    if Growing_Context_Sensitive_Grammar.check_grammar(rules):
        # matching is polynomial
        return Growing_Context_Sensitive_Grammar(non_terminal_set, terminal_set, start_symbol, rules)
    return Recursive_Grammar(non_terminal_set, terminal_set, start_symbol, rules)


if __name__ == "__main__":
    # G = ({S, A}, {a, b}, S, {S → aAb, A → aaAbb, A → ab})
    grammar_1 = build_grammar({"S", "A"}, {"a", "b"}, "S", {
        "S": ["aAb"],
        "A": ["aaAbb", "ab"]
    })

    assert grammar_1.match("aabb") == True
    assert grammar_1.match("aaaabbbb") == True
    assert grammar_1.match("aaabbb") == False

    # G'' = ({S, A, B}, {a, b, c}, S, {S → aAbc, Ab → aAbb, Ac → aaAcc, bA → bbAa, cA → ccAa, Ab → abb, Ac → aac})
    grammar_2 = build_grammar({"S", "A", "B"}, {"a", "b", "c"}, "S", {
        "S": ["aAbc"],
        "Ab": ["aAbb", "abb"],
        "Ac": ["aaAcc", "aac"],
        "bA": ["bbAa"],
        "cA": ["ccAa"]
    })

    assert grammar_2.match("aabbc") == True
    assert grammar_2.match("aaabbbc") == True
    assert grammar_2.match("aaaaaaccc") == False
