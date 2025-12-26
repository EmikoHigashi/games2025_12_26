import tkinter as tk
from tkinter import font
import ast
import operator

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Simple calculator GUI (test.py)
# Usage: python test.py


# Safe expression evaluator using ast
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

def safe_eval(expr: str):
    """
    Evaluate a numeric expression safely supporting + - * / % // ** and parentheses.
    Raises ValueError on invalid expressions.
    """
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                return ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported operator: {op_type}")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                return ALLOWED_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type}")
        if isinstance(node, ast.Num):  # Python <3.8
            return node.n
        if isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numeric constants are allowed")
        if isinstance(node, ast.Call):
            raise ValueError("Function calls not allowed")
        raise ValueError(f"Unsupported expression: {type(node)}")

    parsed = ast.parse(expr, mode='eval')
    return _eval(parsed)


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("電卓")
        self.resizable(False, False)
        self._create_widgets()
        self._bind_keys()

    def _create_widgets(self):
        pad = 8
        self.entry_var = tk.StringVar()
        entry_font = font.Font(size=20)
        btn_font = font.Font(size=14)

        entry = tk.Entry(self, textvariable=self.entry_var, font=entry_font, justify='right', bd=4, relief='sunken')
        entry.grid(row=0, column=0, columnspan=4, padx=pad, pady=(pad, 0), ipady=10, sticky='we')
        entry.focus_set()

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('⌫', 5, 1), ('(', 5, 2), (')', 5, 3),
        ]

        for (text, r, c) in buttons:
            action = (lambda t=text: self._on_button(t))
            b = tk.Button(self, text=text, width=5, height=2, font=btn_font, command=action)
            b.grid(row=r, column=c, padx=4, pady=4, sticky='nsew')

        # Configure grid weights so buttons expand nicely
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)

    def _bind_keys(self):
        for key in '0123456789.+-*/()%':
            self.bind(key, self._on_key)
        self.bind('<Return>', lambda e: self._evaluate())
        self.bind('<KP_Enter>', lambda e: self._evaluate())
        self.bind('<BackSpace>', lambda e: self._backspace())
        self.bind('<Delete>', lambda e: self._clear())
        self.bind('<Escape>', lambda e: self._clear())

    def _on_key(self, event):
        self._append(event.char)

    def _on_button(self, label):
        if label == 'C':
            self._clear()
        elif label == '⌫':
            self._backspace()
        elif label == '=':
            self._evaluate()
        else:
            self._append(label)

    def _append(self, s):
        cur = self.entry_var.get()
        # Simple validation: avoid multiple dots in a single number segment
        self.entry_var.set(cur + s)

    def _clear(self):
        self.entry_var.set('')

    def _backspace(self):
        cur = self.entry_var.get()
        self.entry_var.set(cur[:-1])

    def _evaluate(self):
        expr = self.entry_var.get().strip()
        if not expr:
            return
        try:
            result = safe_eval(expr)
            # Display integer without trailing .0
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.entry_var.set(str(result))
        except Exception:
            self.entry_var.set("Error")

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()