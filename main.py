import tkinter as tk
from calculatorgui import CalculatorApp, ExpressionManager, ExpressionEvaluator


if __name__ == '__main__':
    root = tk.Tk()
    
    # Dependency injection
    expression_manager = ExpressionManager()
    evaluator = ExpressionEvaluator()
    
    app = CalculatorApp(root, expression_manager, evaluator)
    root.mainloop()