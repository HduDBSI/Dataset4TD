from blockMetric import *
code_snippet = """
Do d = new O();
for (File grammarFile : grammarsAndTokens) {
    if (!grammarFile.getName().endsWith(".tokens"))
        analyse(grammarFile, grammarsAndTokens, tool);
}

"""

dic, list, _ = compute_metrics(code_snippet)
print(dic, list)
