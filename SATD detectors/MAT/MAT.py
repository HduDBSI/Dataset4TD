#  reproduction of MAT https://github.com/Naplues/MAT/
#  paper: "How far have we progressed in identifying self-admitted technical debts? 
#         A comprehensive empirical study"
#  https://dl.acm.org/doi/10.1145/3447247
class MAT():
    __keywords = ["todo", "hack", "fixme", "xxx"]
    __TD = 1
    __NonTD = 0
    
    def filter(self, word: str) -> str: 
        res = ""
        for ch in word:
            if ('a' <= ch and ch <= 'z') or ('A' <= ch and ch <= 'Z'):
                res += ch
        return res.lower()


    def splitToTokens(self, comment: str) -> list:
        tokens = comment.split()
        words = []
        for token in tokens:
            word = self.filter(token)
            if 2 < len(word) and len(word) < 20:
                words.append(word)
        return words
    
    def classify(self, comment: str) -> int:
        tokens = self.splitToTokens(comment)
        for token in tokens:
            for keyword in self.__keywords:
                if token.startswith(keyword) or token.endswith(keyword):
                    if "xxx" in token and token != "xxx":
                        return self.__NonTD
                    else:
                        return self.__TD
        return self.__NonTD

# for test
def main():
    mat = MAT()
    comment =  "// hacked ignored attributes in a different NS ( maybe store them ? )"
    res = mat.classify(comment)
    print(res)
    
if __name__=='__main__':
    main()
