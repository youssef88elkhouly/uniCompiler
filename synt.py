import tkinter as tk
from tkinter import ttk, messagebox
import re
import math

class TreeNode:
    def __init__(self, value, arity=2):
        self.value = value
        self.left = None
        self.right = None
        self.arity = arity  # 1 for unary, 2 for binary

class SyntaxAnalyzer:
    def __init__(self):
        # precedence, (precedence, associativity) assoc: 'L' or 'R'
        self.operators = {
            '+': (1, 'L'), '-': (1, 'L'),
            '*': (2, 'L'), '/': (2, 'L'), '%': (2, 'L'),
            '^': (3, 'R'),
            'neg': (4, 'R')  # unary minus
        }

    def tokenize(self, expr):
        expr = expr.strip()
        # insert spaces around parentheses and operators except unary minus handling will be done later
        expr = re.sub(r'([\+\-\*/\^%\(\)])', r' \1 ', expr)
        raw = [t for t in expr.split() if t]
        tokens = []
        for i, t in enumerate(raw):
            if re.fullmatch(r'\d+(\.\d+)?', t):  # number
                tokens.append(('NUMBER', t))
            elif t.isidentifier():  # identifier like x, var1
                tokens.append(('IDENT', t))
            elif t in ('+', '*', '/', '^', '%'):
                tokens.append(('OP', t))
            elif t == '-':
                # unary if at start or after operator or after left paren
                if i == 0 or raw[i-1] in ('+', '-', '*', '/', '^', '%', '('):
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
                stack.pop()  # remove LP
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
                    # binary
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

class TreeDrawer(tk.Tk):
    NODE_RADIUS = 20
    X_GAP = 20
    Y_GAP = 70

    def __init__(self):
        super().__init__()
        self.title("Postfix / Syntax Tree Viewer")
        self.geometry("900x600")
        self.analyzer = SyntaxAnalyzer()
        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill='x', padx=6, pady=6)

        ttk.Label(top, text="Expression (infix):").pack(side='left')
        self.entry = ttk.Entry(top)
        self.entry.pack(side='left', fill='x', expand=True, padx=6)
        self.entry.insert(0, "a + b * (c - d) ^ e")

        ttk.Button(top, text="Draw Tree", command=self.on_draw).pack(side='left', padx=6)
        ttk.Button(top, text="Show Postfix", command=self.on_show_postfix).pack(side='left')

        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill='both', expand=True, padx=6, pady=6)

        bottom = ttk.Frame(self)
        bottom.pack(fill='x', padx=6, pady=4)
        self.postfix_label = ttk.Label(bottom, text="Postfix: ")
        self.postfix_label.pack(side='left')

    def on_show_postfix(self):
        expr = self.entry.get()
        try:
            tokens = self.analyzer.tokenize(expr)
            postfix = self.analyzer.infix_to_postfix(tokens)
            self.postfix_label.config(text="Postfix: " + " ".join(postfix))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_draw(self):
        expr = self.entry.get()
        try:
            tokens = self.analyzer.tokenize(expr)
            postfix = self.analyzer.infix_to_postfix(tokens)
            tree = self.analyzer.build_syntax_tree(postfix)
            self.postfix_label.config(text="Postfix: " + " ".join(postfix))
            self.draw_tree(tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def draw_tree(self, root):
        self.canvas.delete('all')
        if not root:
            return
        # assign x positions via inorder traversal
        positions = {}
        counter = {'x': 0}

        def inorder(node, depth=0):
            if not node:
                return
            if node.left:
                inorder(node.left, depth+1)
            x = counter['x']
            positions[node] = (x, depth)
            counter['x'] += 1
            if node.right:
                inorder(node.right, depth+1)

        inorder(root)

        # compute coordinates scaled to canvas size
        width = max(1, counter['x'])
        canvas_w = max(800, self.canvas.winfo_width())
        canvas_h = max(200, self.canvas.winfo_height())
        x_scale = (canvas_w - 40) / width
        y_scale = self.Y_GAP

        coords = {}
        for node, (ix, depth) in positions.items():
            cx = 20 + ix * x_scale
            cy = 20 + depth * y_scale
            coords[node] = (cx, cy)

        # draw edges first
        for node, (cx, cy) in coords.items():
            if node.left:
                lx, ly = coords[node.left]
                self.canvas.create_line(cx, cy + self.NODE_RADIUS, lx, ly - self.NODE_RADIUS, width=2)
            if node.right:
                rx, ry = coords[node.right]
                self.canvas.create_line(cx, cy + self.NODE_RADIUS, rx, ry - self.NODE_RADIUS, width=2)

        # draw nodes
        for node, (cx, cy) in coords.items():
            self.canvas.create_oval(cx - self.NODE_RADIUS, cy - self.NODE_RADIUS,
                                    cx + self.NODE_RADIUS, cy + self.NODE_RADIUS,
                                    fill='#f0f0f0', outline='black')
            text = str(node.value)
            self.canvas.create_text(cx, cy, text=text, font=('Arial', 10, 'bold'))

if __name__ == "__main__":
    app = TreeDrawer()
    app.mainloop()