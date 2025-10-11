import re

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        
    def __str__(self):
        return str(self.value)
    
    def display(self, level=0):
        ret = "  " * level + str(self.value) + "\n"
        if self.left:
            ret += self.left.display(level + 1)
        if self.right:
            ret += self.right.display(level + 1)
        return ret

class SyntaxAnalyzer:
    def __init__(self):
        self.operators = {
            '+': 1, '-': 1, 
            '*': 2, '/': 2, '%': 2,
            '^': 3
        }
        self.tokens = []
        self.postfix = []
    
    def tokenize(self, expression):
        """Tokenize the modified equation"""
        # Remove spaces and add spaces around operators for easier tokenization
        expression = expression.replace(' ', '')
        
        # Add spaces around operators and parentheses
        expression = re.sub(r'([\+\-\*/\^%\(\)])', r' \1 ', expression)
        
        # Split into tokens and filter out empty strings
        raw_tokens = [token for token in expression.split() if token]
        
        tokens = []
        i = 0
        while i < len(raw_tokens):
            token = raw_tokens[i]
            
            # Check for floating-point numbers
            if self.is_float(token):
                tokens.append(('NUMBER', token))
            elif token in self.operators:
                tokens.append(('OPERATOR', token))
            elif token == '(':
                tokens.append(('LPAREN', token))
            elif token == ')':
                tokens.append(('RPAREN', token))
            elif token.startswith('id'):
                tokens.append(('IDENTIFIER', token))
            else:
                # Handle negative numbers and subtraction
                if token == '-' and (i == 0 or raw_tokens[i-1] in self.operators or raw_tokens[i-1] == '('):
                    if i + 1 < len(raw_tokens) and self.is_float(raw_tokens[i+1]):
                        tokens.append(('NUMBER', '-' + raw_tokens[i+1]))
                        i += 1
                    else:
                        tokens.append(('OPERATOR', token))
                else:
                    tokens.append(('UNKNOWN', token))
            i += 1
        
        self.tokens = tokens
        return tokens
    
    def is_float(self, token):
        """Check if token is a floating-point number"""
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def infix_to_postfix(self, tokens):
        """Convert infix notation to postfix notation"""
        output = []
        stack = []
        
        for token_type, token_value in tokens:
            if token_type == 'NUMBER' or token_type == 'IDENTIFIER':
                output.append(token_value)
            elif token_type == 'LPAREN':
                stack.append(('LPAREN', token_value))
            elif token_type == 'RPAREN':
                while stack and stack[-1][0] != 'LPAREN':
                    output.append(stack.pop()[1])
                stack.pop()  # Remove the left parenthesis
            elif token_type == 'OPERATOR':
                while (stack and stack[-1][0] == 'OPERATOR' and 
                       self.operators.get(stack[-1][1], 0) >= self.operators.get(token_value, 0)):
                    output.append(stack.pop()[1])
                stack.append(('OPERATOR', token_value))
        
        while stack:
            output.append(stack.pop()[1])
        
        self.postfix = output
        return output
    
    def build_syntax_tree(self, postfix):
        """Create a Syntax Tree using the postfix notation"""
        stack = []
        
        for token in postfix:
            if token in self.operators:
                # Operator node
                node = TreeNode(token)
                node.right = stack.pop()
                node.left = stack.pop()
                stack.append(node)
            else:
                # Operand node (number or identifier)
                stack.append(TreeNode(token))
        
        return stack[0] if stack else None

# Main execution
code = input("waiting for input: ")
code += " "
newcode = ""
length = len(code)
idcounter = 1
skip = 0
reserved = ["if","else","while","for","return","class","import","from","break","continue","in","not","and","or","is","None","True","False","print"]

allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=+-*/^%()_. ")

print("\n=== LEXICAL ANALYSIS ===")
for i in range(length):
    if skip > 0:
        skip -= 1
        continue

    if code[i] not in allowed_chars:
        raise ValueError(f"Invalid character '{code[i]}' at position {i}")
    
    if code[i].isalpha():
        flag = True
        sindex = i
        eindex = i
        index = i
        while flag:
            index += 1
            if index < length and (code[index].isalpha() or code[index].isdigit() or code[index] == "_"):
                eindex = index
            else:
                flag = False
        
        word = code[sindex:eindex+1]

        if word in reserved:
            newcode += word
        else:
            newcode += "id" + str(idcounter) 
            idcounter += 1

        skip = eindex - sindex
    elif code[i] == "=":
        newcode += "="
    elif code[i] == "+":
        newcode += "+"
    elif code[i] == "-":
        newcode += "-"
    elif code[i] == "*":
        newcode += "*"
    elif code[i] == "/":
        newcode += "/"
    elif code[i] == "^":
        newcode += "^"
    elif code[i] == "%":
        newcode += "%"
    elif code[i] == "(":
        newcode += "("
    elif code[i] == ")":
        newcode += ")"
    elif code[i] == ".":
        newcode += "."
    elif code[i].isdigit():
        newcode += code[i]

print(f"Tokenized expression: {newcode}")

print("\n=== SYNTAX ANALYZER ===")

# Create syntax analyzer instance
analyzer = SyntaxAnalyzer()

# a. Tokenize the modified equation
print("a. Tokenizing the modified equation...")
tokens = analyzer.tokenize(newcode)
print(f"   Tokens: {tokens}")

# b. Check for special cases like floating-point numbers
print("b. Checking for floating-point numbers...")
float_tokens = [token for token_type, token_value in tokens if token_type == 'NUMBER' and '.' in token_value]
if float_tokens:
    print(f"   Floating-point numbers found: {float_tokens}")
else:
    print("   No floating-point numbers found")

# c. Convert the expression from infix notation to postfix
print("c. Converting to postfix notation...")
postfix = analyzer.infix_to_postfix(tokens)
print(f"   Postfix notation: {' '.join(postfix)}")

# d. Create a Syntax Tree using the postfix notation
print("d. Creating syntax tree...")
syntax_tree = analyzer.build_syntax_tree(postfix)

# e. OUTPUT: Syntax Tree
print("e. OUTPUT: Syntax Tree")
if syntax_tree:
    print("\nSyntax Tree Structure:")
    print(syntax_tree.display())
else:
    print("No syntax tree could be created")