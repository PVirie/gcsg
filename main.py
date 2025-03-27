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
        for p, a, b, s in self.rules[self.S]:
            if b == "":
                self.has_epsilon_rule = True
                break


    def try_replace(self, x, reachable_set):
        # for all non-terminal symbol in x, try to replace it with reachable_set
        if len(x) == 0:
            yield ""
        else:
            # recursive
            for i in range(1, len(x) + 1):
                if x[:i] in self.non_terminal_set:
                    for replacement in reachable_set[x[:i]]:
                        for suffix in self.try_replace(x[i:], reachable_set):
                            yield replacement + suffix
                    break
                else:
                    if x[:i] in self.terminal_set:
                        for suffix in self.try_replace(x[i:], reachable_set):
                            yield x[:i] + suffix
                    else:
                        break


    def compute_possible_source(self, lhs, rhs, target, reachable_set):
        # compute possible lhs of a given production rule
        # lhs -> rhs which may contain non-terminal
        # the goal is to match target
        # rhs = (prefix, a, b, suffix)
        prefix, center_a, center_b, suffix = rhs
        for p in self.try_replace(prefix, reachable_set):
            for b in self.try_replace(center_b, reachable_set):
                for s in self.try_replace(suffix, reachable_set):
                    if p + b + s == target:
                        for a in self.try_replace(center_a, reachable_set):
                            yield p + a + s


    def match(self, x: str) -> bool:
        # matching is polynomial
        L = len(x)
        N = len(self.non_terminal_set)
        reachable_set = {}
        for nt in self.non_terminal_set:
            reachable_set[nt] = set()
            
        if L == 0:
            return self.has_epsilon_rule
        
        for i in range(L):
            for nt in self.non_terminal_set:
                for rule in self.rules[nt]:
                    if rule[2] == x[i]:
                        reachable_set[nt].add(x[i])

        for l in range(2, L + 1):
            for i in range(L - l + 1):
                j = i + l
                substr = x[i:j]
                for nt in self.non_terminal_set:
                    for lhs, rhses in self.rules.items():
                        for rhs in rhses:
                            # iterate subset in subset
                            for lhs_ in self.compute_possible_source(lhs, rhs, substr, reachable_set):
                                if lhs_ in reachable_set[nt]:
                                    reachable_set[nt].add(substr)
                                    break

        return x in reachable_set[self.S]

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
