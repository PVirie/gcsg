"""
    CYK Algorithm; polynomial time O(n^3)|G|, where |G| is the number of production rules

    Need to convert rules into the Chomsky Normal Form (CNF) first
    where A, B, and C are nonterminal symbols, the letter a is a terminal symbol (a symbol that represents a constant value), S is the start symbol, and ε denotes the empty string. Also, neither B nor C may be the start symbol, and the third production rule can only appear if ε is in L(G), the language produced by the context-free grammar G.

    START: Eliminate the start symbol from right-hand sides
    TERM: Eliminate rules with nonsolitary terminals
    BIN: Eliminate right-hand sides with more than 2 nonterminals
    DEL: Eliminate ε-rules
    UNIT: Eliminate unit rules    
"""

def get_next_free_letter(non_terminal_set, terminal_set):
    # consider used letters
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
        if letter not in non_terminal_set and letter not in terminal_set:
            return letter
    # generate random unicode
    while True:
        letter = chr(np.random.randint(0, 0x10FFFF))
        if letter not in non_terminal_set and letter not in terminal_set:
            return letter

def TERM(non_terminal_set, terminal_set, start_symbol, rules: dict):
    #     A → X1 ... a ... Xn
    #     with a terminal symbol a being not the only symbol on the right-hand side, introduce, for every such terminal, a new nonterminal symbol Na, and a new rule
    #     Na → a.
    #     Change every rule A → X1 ... a ... Xn to A → X1 ... Na ... Xn.

    new_non_terminal_set = set()
    new_non_terminal_set.update(non_terminal_set)

    new_rules = {}
    for nt, productions in rules.items():
        new_rules[nt] = []
        for prod in productions:
            new_prod = ""
            for p in prod:
                if p in terminal_set and len(prod) > 1:
                    new_nt = get_next_free_letter(new_non_terminal_set, terminal_set)
                    new_non_terminal_set.add(new_nt)
                    new_rules[new_nt] = [p]
                    new_prod += new_nt
                else:
                    new_prod += p
            new_rules[nt].append(new_prod)

    return new_non_terminal_set, terminal_set, start_symbol, new_rules


def BIN(non_terminal_set, terminal_set, start_symbol, rules: dict):
    # Replace each rule A → X1 X2 ... Xn
    # with more than 2 nonterminals X1,...,Xn by rules
    # A → X1 A1,
    # A1 → X2 A2,
    # ... ,
    # An-2 → Xn-1 Xn,
    # where A1,...,An-1 are new nonterminal symbols.
    new_non_terminal_set = set()
    new_non_terminal_set.update(non_terminal_set)
    new_rules = {}
    for nt, productions in rules.items():
        new_rules[nt] = []
        for prod in productions:
            if len(prod) > 2:
                A = get_next_free_letter(new_non_terminal_set, terminal_set)
                new_non_terminal_set.add(A)
                new_rules[nt].append(prod[0] + A)
                for i in range(1, len(prod) - 2):
                    A_ = get_next_free_letter(new_non_terminal_set, terminal_set)
                    new_non_terminal_set.add(A_)
                    new_rules[A] = [prod[i] + A_]
                    A = A_
                new_rules[A] = [prod[-2] + prod[-1]]
            else:
                new_rules[nt].append(prod)
            
    return new_non_terminal_set, terminal_set, start_symbol, new_rules



def DEL(non_terminal_set, terminal_set, start_symbol, rules: dict):
    # An ε-rule is a rule of the form
    # A → ε,
    # where A is not S0, the grammar's start symbol.
    # To eliminate all rules of this form, first determine the set of all nonterminals that derive ε.
    # If a rule A → ε exists, then A is nullable.
    # If a rule A → X1 ... Xn exists, and every single Xi is nullable, then A is nullable, too.
    # Obtain an intermediate grammar by replacing each rule
    # A → X1 ... Xn
    # by all versions with some nullable Xi omitted. 
    # By deleting in this grammar each ε-rule, unless its left-hand side is the start symbol, the transformed grammar is obtained.

    nullable_rules = set()
    for nt, productions in rules.items():
        for prod in productions:
            if len(prod) == 0 and nt != start_symbol:
                nullable_rules.add(nt)

    added = True
    while added:
        added=False
        for nt, productions in rules.items():
            for prod in productions:
                if all([x in nullable_rules for x in prod]):
                    if nt not in nullable_rules:
                        nullable_rules.add(nt)
                        added = True

    new_rules = {}
    for nt, productions in rules.items():
        new_rules[nt] = []
        for prod in productions:
            if len(prod) == 0:
                continue
            if all([x in nullable_rules for x in prod]):
                new_prod = ""
                for x in prod:
                    if x not in nullable_rules:
                        new_prod += x
                new_rules[nt].append(new_prod)
            else:
                new_rules[nt].append(prod)

    return non_terminal_set, terminal_set, start_symbol, new_rules


def UNIT(non_terminal_set, terminal_set, start_symbol, rules: dict):
    # A unit rule is a rule of the form A → B,
    # where A, B are nonterminal symbols. To remove it, for each rule
    # B → X1 ... Xn,
    # where X1 ... Xn is a string of nonterminals and terminals, add rule
    # A → X1 ... Xn
    # unless this is a unit rule which has already been (or is being) removed. 
    # The skipping of nonterminal symbol B in the resulting grammar is possible due to B being a member of the unit closure of nonterminal symbol A.

    unit_replacement = {}
    for nt, productions in rules.items():
        for prod in productions:
            if len(prod) == 1 and prod[0] in non_terminal_set:
                unit_replacement[prod[0]] = nt

    new_rules = {}
    for nt, productions in rules.items():
        for prod in productions:
            if len(prod) == 1 and prod[0] in non_terminal_set:
                continue
            if nt in unit_replacement:
                new_nt = unit_replacement[nt]
                if new_nt not in new_rules:
                    new_rules[new_nt] = []
                new_rules[new_nt].append(prod)
            if nt not in new_rules:
                new_rules[nt] = []
            new_rules[nt].append(prod)

    return non_terminal_set, terminal_set, start_symbol, new_rules


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
        T = len(self.terminal_set)
        nt_to_index = {nt: i for i, nt in enumerate(self.non_terminal_set)}
        # initialize the table
        table = np.zeros((L, L, NT), dtype=bool)
        # fill the table
        for i in range(L):
            for nt, productions in self.rules.items():
                for prod in productions:
                    if len(prod) == 1 and prod[0] in self.terminal_set:
                        if prod[0] == x[i]:
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