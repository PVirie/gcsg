
class Recursive_Grammar:

    def __init__(self, non_terminal_set, terminal_set, start_symbol, rules: dict):
        self.non_terminal_set = non_terminal_set
        self.terminal_set = terminal_set
        self.S = start_symbol
        self.rules = rules
        self.has_epsilon_rule = False

        self._reverse_rules = {}
        for nt, productions in rules.items():
            for prod in productions:
                if prod not in self._reverse_rules:
                    self._reverse_rules[prod] = []
                self._reverse_rules[prod].append(nt)

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
                replacements = self._reverse_rules.get(substr, [])
                for r in replacements:
                    if self.match(x[:j] + r + x[i:], cache):
                        cache[x] = True
                        return True
        cache[x] = False
        return False
    

    @staticmethod
    def check_grammar(rules: dict):
        return True
