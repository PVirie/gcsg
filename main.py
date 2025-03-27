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


    # growing context sensitive grammar
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


    # unrestricted grammar not context free nor growing context sensitive nor context sensitive, may never halt
    grammar_4 = grammars.build_grammar({"S", "A"}, {"a", "b"}, "S", {
        "S": ["aS", "Sb", "A"],
        "aAb": ["b"]
    })

    assert grammar_4.match("b") == True
    assert grammar_4.match("ab") == True
    assert grammar_4.match("aaab") == True
    assert grammar_4.match("bbbb") == True


    # growing context sensitive grammar
    grammar_5 = grammars.build_grammar({"S", "A", "B"}, {"a", "b", "c"}, "S", {
        "S": ["aABb", "aa"],
        "A": ["aABb", "aa"],
        "B": ["bABc", "bb"],
        "aAB": ["aBBB"],
        "bAB": ["bBBB"],
    })

    assert grammar_5.match("aa") == True
    assert grammar_5.match("aaabbb") == True
    assert grammar_5.match("aabbbbbbbbbbbbbbcb") == True
    assert grammar_5.match("ccccaaaaabbbbbb") == False
