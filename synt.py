# synt.py
import re

class TreeNode:
    def __init__(self, value, arity=2):
        self.value = value
        self.left = None
        self.right = None
        self.arity = arity  # 1 for unary, 2 for binary

class SyntaxAnalyzer:
    def __init__(self):
        self.operators = {
            '=': (0, 'R'),  # Assignment (lowest precedence, right-associative)
            '+': (1, 'L'), '-': (1, 'L'),
            '*': (2, 'L'), '/': (2, 'L'), '%': (2, 'L'),
            '^': (3, 'R'),
            'neg': (4, 'R')  # unary minus
        }

    def tokenize(self, expr):
        expr = expr.strip()
        # Insert spaces around operators and parentheses
        expr = re.sub(r'([=\+\-\*/\^%\(\)])', r' \1 ', expr)
        raw = [t for t in expr.split() if t]
        tokens = []
        
        for i, t in enumerate(raw):
            if re.fullmatch(r'\d+(\.\d+)?', t):  # number
                tokens.append(('NUMBER', t))
            elif t.isidentifier():  # identifier like x, var1
                tokens.append(('IDENT', t))
            elif t in ('+', '*', '/', '^', '%', '='):
                tokens.append(('OP', t))
            elif t == '-':
                # unary if at start or after operator or after left paren
                if i == 0 or raw[i-1] in ('=', '+', '-', '*', '/', '^', '%', '('):
                    tokens.append(('OP', 'neg'))
                else:
                    tokens.append(('OP', '-'))
            elif t == '(':
                tokens.append(('LP', t))
            elif t == ')':
                tokens.append(('RP', t))
            else:
                tokens.append(('UNK', t))
        return tokens

    def infix_to_postfix(self, tokens):
        out = []
        stack = []
        for typ, val in tokens:
            if typ in ('NUMBER', 'IDENT'):
                out.append(val)
            elif typ == 'OP':
                prec, assoc = self.operators[val]
                while stack and stack[-1][0] == 'OP':
                    top = stack[-1][1]
                    top_prec, top_assoc = self.operators[top]
                    if (assoc == 'L' and prec <= top_prec) or (assoc == 'R' and prec < top_prec):
                        out.append(stack.pop()[1])
                    else:
                        break
                stack.append(('OP', val))
            elif typ == 'LP':
                stack.append(('LP', val))
            elif typ == 'RP':
                while stack and stack[-1][0] != 'LP':
                    out.append(stack.pop()[1])
                if not stack:
                    raise ValueError("Mismatched parentheses")
                stack.pop()
            else:
                raise ValueError(f"Unknown token {val}")
        while stack:
            if stack[-1][0] == 'LP' or stack[-1][0] == 'RP':
                raise ValueError("Mismatched parentheses")
            out.append(stack.pop()[1])
        return out

    def build_syntax_tree(self, postfix):
        stack = []
        for tok in postfix:
            if tok in self.operators:
                if tok == 'neg':
                    node = TreeNode('-', arity=1)
                    if not stack:
                        raise ValueError("Invalid expression for unary operator")
                    node.right = stack.pop()
                    stack.append(node)
                else:
                    # For assignment, it's binary but we need to handle it specially
                    if len(stack) < 2:
                        raise ValueError("Invalid expression for binary operator")
                    right = stack.pop()
                    left = stack.pop()
                    node = TreeNode(tok, arity=2)
                    node.left = left
                    node.right = right
                    stack.append(node)
            else:
                stack.append(TreeNode(tok, arity=0))
        return stack[0] if stack else None

    def analyze_expression(self, expr):
        tokens = self.tokenize(expr)
        postfix = self.infix_to_postfix(tokens)
        tree = self.build_syntax_tree(postfix)
        return {
            'tokens': tokens,
            'postfix': postfix,
            'tree': tree
        }

# Test function when run directly
if __name__ == "__main__":
    analyzer = SyntaxAnalyzer()
    expr = input("Enter expression for syntax analysis: ")
    result = analyzer.analyze_expression(expr)
    print(f"Tokens: {result['tokens']}")
    print(f"Postfix: {' '.join(result['postfix'])}")
    print(f"Tree root: {result['tree'].value if result['tree'] else 'None'}")