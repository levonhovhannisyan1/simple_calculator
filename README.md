# simple_calculator
🧮 Python GUI Calculator
A modern, feature-rich calculator application built with Python and Tkinter, featuring a clean dark theme interface and simple but detailed mathematical operations.

✨ Features

Modern Dark Theme UI - Sleek interface with professional styling
Comprehensive Operations - Basic arithmetic, percentages, sign toggle
Expression History - View your current calculation and result
Input Validation - Smart input handling prevents invalid expressions
Error Handling - Graceful error management for invalid operations
Responsive Design - Clean button layout with hover effects
Decimal Support - Full floating-point number support
Scientific Notation - Automatic formatting for very large/small numbers

🛠️ Installation
Prerequisites

Python 3.7 or higher
tkinter (usually included with Python)

📁 Project Structure
simple_calculator/
│
├── main.py            # Application entry point
├── calculator.py      # Core calculator logic and GUI
├── config.py          # Configuration constants
├── utilities.py       # Helper functions
├── README.md          # Project documentation
└── screenshot.png     # Application screenshot

🎯 Usage
Basic Operations

Numbers: Click digit buttons (0-9)
Operators: +, -, ×, ÷
Decimal: . for decimal numbers
Equals: = to calculate result

Advanced Features

Sign Toggle: ± to change number sign
Percentage: % for percentage calculations
Clear Last: ⟵ to remove last input
Clear All: ⟸ to reset calculator

Example Calculations
Basic: 15 + 25 = 40
Decimal: 3.14 × 2 = 6.28
Percentage: 90 + 450% = 495
Mixed: 90+450%+3.14×9×9=(-12) = 473.805

🏗️ Architecture
The calculator follows a clean, modular architecture:
Core Components

InputValidator - Validates user input according to business rules
ExpressionBuilder - Constructs and modifies mathematical expressions
CalculationState - Manages calculator state and expression history
ExpressionManager - Coordinates input validation and expression building
ExpressionEvaluator - Handles mathematical evaluation and result formatting
CalculatorApp - Main GUI application class

🧪 Testing
The calculator includes comprehensive input validation and error handling:

Input Validation: Prevents invalid symbols formats(unlike many default calculators, such as the Ubuntu calculator(shown in screenshot))
Operator Logic: Smart operator replacement and validation
Edge Cases: Handles division by zero, overflow, underflow
Expression Parsing: Robust parsing of complex expressions

👨‍💻 Author
Levon Hovhannisyan

GitHub: @levonhovhannisyan1
LinkedIn: linkedin.com/in/levonhovhannisyan
Email: levon.hovhannisyan1010@gmail.com

🙏 Acknowledgments

Built with Python and Tkinter
Inspired by modern calculator designs
Thanks to the Python community for excellent documentation


⭐ If you found this project helpful, please give it a star! ⭐
