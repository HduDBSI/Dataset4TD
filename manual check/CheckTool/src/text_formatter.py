import re
from html import escape

class TextFormatter():
    __replacement1 = r'<font color="red">\1</font>'
    __replacement2 = r'<font color="lightblue">\1</font>'
    __pattern1 = r'(\/\/|\*\/|\*|\/\*)' # match '/*', '*/', '*' , '//'
    __pattern2 = r'\s+' # match continous blank 

    def __init__(self, keyword1, keyword2):
        self.__keywords1 = keyword1
        self.__keywords2 = keyword2
    
    def format(self, text:str) -> str:
        text = self.highlight_keywords(text)
        text = self.add_newlines(text)
        return text
    
    def remove_comment_symbols(self, text: str) -> str:
        text = re.sub(self.__pattern1, ' ', text)
        text = re.sub(self.__pattern2, ' ', text)
        return text
    
    def add_newlines(self, text: str) -> str:
        # Define the regular expression pattern
        pattern = r"(//|\s{4,}|/\*|\*/|\*\s{2,})"

        # Use re.sub() to insert <br> before "//" or consecutive spaces
        new_text = re.sub(pattern, r"<br>\1", text)
        
        # new_text = re.sub(r"<br\s*/?>+", "<br>", new_text)
        return new_text.strip("<br>")

    def highlight_keywords(self, text:str) -> str:
        text = escape(text)
        for keyword in self.__keywords1:
            pattern = re.compile(f'({re.escape(keyword)})', re.IGNORECASE)
            text = pattern.sub(self.__replacement1, text)
        for keyword in self.__keywords2:
            pattern = re.compile(f'({re.escape(keyword)})', re.IGNORECASE)
            text = pattern.sub(self.__replacement2, text)
        return text.strip()

def test():
    keyword1 = ["happy", "joyful"]
    keyword2 = ["sad", "painful"]
    tf = TextFormatter(keyword1, keyword2)
    text = "// You are happy, i am painful.   // You are sad, i am joyful."
    print(tf.format(text))

if __name__ == "__main__":
    test()