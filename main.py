import grammars


if __name__ == "__main__":

    # context free grammar
    grammar_1 = grammars.build_grammar({"S", "A"}, {"a", "b"}, "S", {
        "S": ["aAb"],
        "A": ["aaAbb", "ab"]
    })

    assert grammar_1.match("aabb") == True
    assert grammar_1.match("aaaabbbb") == True
    assert grammar_1.match("aaabbbb") == False
    assert grammar_1.match("aaabbb") == False

    # G'' = ({S, A, B}, {a, b, c}, S, {S → aAbc, Ab → aAbb, Ac → aaAcc, bA → bbAa, cA → ccAa, Ab → abb, Ac → aac})
    grammar_2 = grammars.build_grammar({"S", "A", "B"}, {"a", "b", "c"}, "S", {
        "S": ["aAbc"],
        "Ab": ["aAbb", "abb"],
        "Ac": ["aaAcc", "aac"],
        "bA": ["bbAa"],
        "cA": ["ccAa"]
    })

    assert grammar_2.match("aabbc") == True
    assert grammar_2.match("aaabbbc") == True
    assert grammar_2.match("aaaaaaccc") == False


    # context free grammar
    grammar_3 = grammars.build_grammar({"S", "A"}, {"a", "b"}, "S", {
        "S": ["aSA", "b"],
        "A": ["b"]
    })

    assert grammar_3.match("abb") == True
    assert grammar_3.match("aabbb") == True
    assert grammar_3.match("bb") == False
