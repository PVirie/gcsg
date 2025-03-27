from .recursive import Recursive_Grammar
from .growing_cs import Growing_Context_Sensitive_Grammar
from .context_free import Context_Free_Grammar



def build_grammar(non_terminal_set, terminal_set, start_symbol, rules):
    if Context_Free_Grammar.check_grammar(non_terminal_set, terminal_set, start_symbol, rules):
        print("Context Free Grammar")
        return Context_Free_Grammar(non_terminal_set, terminal_set, start_symbol, rules)
    if Growing_Context_Sensitive_Grammar.check_grammar(non_terminal_set, terminal_set, start_symbol, rules):
        # matching is polynomial
        return Growing_Context_Sensitive_Grammar(non_terminal_set, terminal_set, start_symbol, rules)
    print("Recursive Grammar")
    return Recursive_Grammar(non_terminal_set, terminal_set, start_symbol, rules)
