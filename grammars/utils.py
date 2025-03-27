"""
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
