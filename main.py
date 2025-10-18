# main.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import lex
import synt

class CompilerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Compiler - Lexical & Syntax Analyzer with Tree Visualization")
        self.root.geometry("1200x800")
        
        self.lex_analyzer = lex.LexicalAnalyzer()
        self.syn_analyzer = synt.SyntaxAnalyzer()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding=10)
        input_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(input_frame, text="Enter code or expression:").pack(anchor='w')
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=4, width=80)
        self.input_text.pack(fill='x', pady=5)
        self.input_text.insert('1.0', "x = a + b * (c - d) ^ e")
        
        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Lexical Analysis", 
                  command=self.run_lexical_analysis).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="Syntax Analysis", 
                  command=self.run_syntax_analysis).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Full Analysis", 
                  command=self.run_full_analysis).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_all).pack(side='left', padx=5)
        
        # Results section
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill='both', expand=True)
        
        # Left side - Text results
        left_frame = ttk.Frame(results_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Lexical results
        self.lex_frame = ttk.LabelFrame(left_frame, text="Lexical Analysis Results", padding=10)
        self.lex_frame.pack(fill='x', pady=(0, 10))
        
        self.lex_output = scrolledtext.ScrolledText(self.lex_frame, height=6, width=60)
        self.lex_output.pack(fill='both', expand=True)
        
        # Syntax results
        self.syn_frame = ttk.LabelFrame(left_frame, text="Syntax Analysis Results", padding=10)
        self.syn_frame.pack(fill='both', expand=True)
        
        self.syn_output = scrolledtext.ScrolledText(self.syn_frame, height=8, width=60)
        self.syn_output.pack(fill='both', expand=True)
        
        # Right side - Tree visualization
        right_frame = ttk.LabelFrame(results_frame, text="Syntax Tree Visualization", padding=10)
        right_frame.pack(side='right', fill='both', expand=True)
        
        self.tree_canvas = tk.Canvas(right_frame, bg='white', width=400, height=500)
        self.tree_canvas.pack(fill='both', expand=True)
        
    def run_lexical_analysis(self):
        try:
            code = self.input_text.get('1.0', 'end-1c').strip()
            if not code:
                messagebox.showwarning("Warning", "Please enter some code")
                return
                
            result, tokens = self.lex_analyzer.analyze(code)
            
            self.lex_output.delete('1.0', 'end')
            self.lex_output.insert('1.0', f"Input: {code}\n")
            self.lex_output.insert('end', f"Output: {result}\n\n")
            self.lex_output.insert('end', "Detailed Tokens:\n")
            for token in tokens:
                self.lex_output.insert('end', f"  {token}\n")
                
            # Clear syntax results and tree
            self.syn_output.delete('1.0', 'end')
            self.tree_canvas.delete('all')
            
        except Exception as e:
            messagebox.showerror("Error", f"Lexical Analysis Error: {e}")
    
    def run_syntax_analysis(self):
        try:
            expr = self.input_text.get('1.0', 'end-1c').strip()
            if not expr:
                messagebox.showwarning("Warning", "Please enter an expression")
                return
                
            result = self.syn_analyzer.analyze_expression(expr)
            
            self.syn_output.delete('1.0', 'end')
            self.syn_output.insert('1.0', f"Input: {expr}\n")
            self.syn_output.insert('end', f"Tokens: {result['tokens']}\n")
            self.syn_output.insert('end', f"Postfix: {' '.join(result['postfix'])}\n")
            self.syn_output.insert('end', f"Tree Root: {result['tree'].value if result['tree'] else 'None'}\n")
            
            # Draw the tree
            if result['tree']:
                self.draw_tree(result['tree'])
            else:
                self.tree_canvas.delete('all')
                self.tree_canvas.create_text(200, 250, text="No tree to display", font=('Arial', 12))
                
        except Exception as e:
            messagebox.showerror("Error", f"Syntax Analysis Error: {e}")
    
    def run_full_analysis(self):
        try:
            code = self.input_text.get('1.0', 'end-1c').strip()
            if not code:
                messagebox.showwarning("Warning", "Please enter some code")
                return
            
            # Run lexical analysis
            lex_result, tokens = self.lex_analyzer.analyze(code)
            
            self.lex_output.delete('1.0', 'end')
            self.lex_output.insert('1.0', f"Input: {code}\n")
            self.lex_output.insert('end', f"Output: {lex_result}\n\n")
            self.lex_output.insert('end', "Detailed Tokens:\n")
            for token in tokens:
                self.lex_output.insert('end', f"  {token}\n")
            
            # Run syntax analysis (using original code)
            syn_result = self.syn_analyzer.analyze_expression(code)
            
            self.syn_output.delete('1.0', 'end')
            self.syn_output.insert('1.0', f"Input: {code}\n")
            self.syn_output.insert('end', f"Tokens: {syn_result['tokens']}\n")
            self.syn_output.insert('end', f"Postfix: {' '.join(syn_result['postfix'])}\n")
            self.syn_output.insert('end', f"Tree Root: {syn_result['tree'].value if syn_result['tree'] else 'None'}\n")
            
            # Draw the tree
            if syn_result['tree']:
                self.draw_tree(syn_result['tree'])
            else:
                self.tree_canvas.delete('all')
                self.tree_canvas.create_text(200, 250, text="No tree to display", font=('Arial', 12))
                
        except Exception as e:
            messagebox.showerror("Error", f"Analysis Error: {e}")
    
    def draw_tree(self, root):
        self.tree_canvas.delete('all')
        if not root:
            return
            
        # Calculate node positions
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
        
        # Scale positions to canvas
        width = max(1, counter['x'])
        canvas_w = self.tree_canvas.winfo_width()
        canvas_h = self.tree_canvas.winfo_height()
        x_scale = (canvas_w - 40) / width if width > 0 else 1
        y_scale = 70
        
        coords = {}
        for node, (ix, depth) in positions.items():
            cx = 20 + ix * x_scale
            cy = 20 + depth * y_scale
            coords[node] = (cx, cy)
        
        # Draw edges
        for node, (cx, cy) in coords.items():
            if node.left and node.left in coords:
                lx, ly = coords[node.left]
                self.tree_canvas.create_line(cx, cy + 20, lx, ly - 20, width=2, fill='black')
            if node.right and node.right in coords:
                rx, ry = coords[node.right]
                self.tree_canvas.create_line(cx, cy + 20, rx, ry - 20, width=2, fill='black')
        
        # Draw nodes
        for node, (cx, cy) in coords.items():
            self.tree_canvas.create_oval(cx - 20, cy - 20, cx + 20, cy + 20, 
                                       fill='lightblue', outline='black', width=2)
            text = str(node.value)
            self.tree_canvas.create_text(cx, cy, text=text, font=('Arial', 10, 'bold'))
    
    def clear_all(self):
        self.input_text.delete('1.0', 'end')
        self.lex_output.delete('1.0', 'end')
        self.syn_output.delete('1.0', 'end')
        self.tree_canvas.delete('all')
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CompilerGUI()
    app.run()