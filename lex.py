# lex.py
class LexicalAnalyzer:
    def __init__(self):
        self.reserved = ["if", "else", "while", "for", "return", "class", "import", 
                        "from", "break", "continue", "in", "not", "and", "or", 
                        "is", "None", "True", "False", "print"]
        
        self.allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=+-*/^%()_. ")

    def analyze(self, code):
        code += " "
        newcode = ""
        lenght = len(code)
        idcounter = 1
        skip = 0
        tokens = []  # Return detailed token information
        
        for i in range(lenght):
            if skip > 0:
                skip -= 1
                continue

            if code[i] not in self.allowed_chars:
                raise ValueError(f"Invalid character '{code[i]}' at position {i}")
            
            if code[i].isalpha():
                flag = True
                sindex = i
                eindex = i
                index = i
                while flag:
                    index += 1
                    if code[index].isalpha() or code[index].isdigit() or code[index] == "_":
                        eindex = index
                    else:
                        flag = False
                
                word = code[sindex:eindex+1]

                if word in self.reserved:
                    newcode += word
                    tokens.append(('RESERVED', word))
                else:
                    newcode += "id" + str(idcounter)
                    tokens.append(('IDENTIFIER', f"id{idcounter}", word))
                    idcounter += 1

                skip = eindex - sindex
            
            elif code[i] == "=":
                newcode += "="
                tokens.append(('OPERATOR', '='))
            elif code[i] == "+":
                newcode += "+"
                tokens.append(('OPERATOR', '+'))
            elif code[i] == "-":
                newcode += "-"
                tokens.append(('OPERATOR', '-'))
            elif code[i] == "*":
                newcode += "*"
                tokens.append(('OPERATOR', '*'))
            elif code[i] == "/":
                newcode += "/"
                tokens.append(('OPERATOR', '/'))
            elif code[i] == "^":
                newcode += "^"
                tokens.append(('OPERATOR', '^'))
            elif code[i] == "%":
                newcode += "%"
                tokens.append(('OPERATOR', '%'))
            elif code[i] == "(":
                newcode += "("
                tokens.append(('DELIMITER', '('))
            elif code[i] == ")":
                newcode += ")"
                tokens.append(('DELIMITER', ')'))
            elif code[i] == ".":
                newcode += "."
                tokens.append(('DELIMITER', '.'))
            elif code[i].isdigit():
                newcode += code[i]
                # Handle multi-digit numbers
                if i == 0 or not code[i-1].isdigit():
                    num = code[i]
                    j = i + 1
                    while j < len(code) and code[j].isdigit():
                        num += code[j]
                        j += 1
                    tokens.append(('NUMBER', num))
                    skip = len(num) - 1
        
        return newcode, tokens

# Test function when run directly
if __name__ == "__main__":
    analyzer = LexicalAnalyzer()
    code = input("Enter code for lexical analysis: ")
    result, tokens = analyzer.analyze(code)
    print(f"Lexical output: {result}")
    print(f"Tokens: {tokens}")