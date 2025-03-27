# Growing Context-Sensitive Grammars Parser

According to the Chomsky hierarchy, Growing context sensitive grammar is a type of context sensitive grammar that the production rule always increase in length.
The complexity of the membership problem is in polynomial time. But it's very hard to implement even for the most capable AI of 2025.
In this repository, I try to do just that. Along with the baseline, recursive grammar and context-free grammar.

## Theory

A simplified proof sketch for the polynomial-time membership of growing context-sensitive grammars can be articulated using a dynamic programming framework . Let G = (N, T, S, P) be a GCSG and w be an input string of length n. The goal is to determine if w ∈ L(G). We can employ a table-based approach to keep track of which non-terminal symbols can derive which substrings of w.

Consider all possible substrings of w. For each substring and each non-terminal A in N, we want to determine if A can derive that substring. We can start by examining substrings of length 1. For every non-terminal A and every terminal a in T, if there is a production rule A → a in P, then the substring of w of length 1 consisting of a can be derived from A.

Next, we consider substrings of increasing length, from 2 up to n. For a substring of length len starting at index i and ending at index j (where len = j - i + 1), we look at all production rules in P. If there is a rule α → β where the length of β is len and the length of α is less than len, we try to see if the sequence of symbols in β can be matched with the substring w[i...j]. Since β might consist of both terminals and non-terminals, if a symbol in β is a terminal, it must match the corresponding character in w[i...j]. If a symbol in β is a non-terminal, say B, we check if we have already determined that B can derive the corresponding substring of w[i...j] in our dynamic programming table.

The crucial aspect here is that because the grammar is growing, the right-hand side of any production rule used to derive a substring of length len must have been formed from a left-hand side of a shorter length. This allows us to build up our knowledge of derivable substrings in increasing order of length. We continue this process until we consider substrings of length n. Finally, we check if the start symbol S can derive the entire input string w. The number of substrings is O(n<sup>2</sup>), and for each substring, we iterate through the production rules (a constant number for a fixed grammar) and consider possible splits of the substring, leading to an overall polynomial time complexity. This dynamic programming approach, which can be seen as a generalization of the Cocke-Kasami-Younger (CYK) algorithm used for context-free grammars, effectively leverages the length-increasing property of GCSGs .
