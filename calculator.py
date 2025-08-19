import tkinter as tk
import re
from config import CalculatorConfig, DisplayConfig
from utilities import _get_button_colors


class InputValidator:
    '''Validates calculator input according to business rules'''
    
    @staticmethod
    def can_append_digit(expression, digit):
        '''
        Checks if digit can be appended to expression.
        
        Args:
            expression (str): Current expression
            digit (str): Digit to append
            
        Returns:
            bool: True if digit can be appended
        '''
        if not expression:
            if digit == '0':
                return False
            return True
        
        last_char = expression[-1]
            
        if len(expression) >= 2 and last_char == '0':
            if expression[-2] in CalculatorConfig.OPERATORS + ['%']:
                return False
                
        if expression and last_char == '%':
            return False
            
        return True
    
    @staticmethod
    def can_append_operator(expression):
        '''
        Checks if operator can be appended to expression.
        
        Args:
            expression (str): Current expression
            operator (str): Operator to append
            
        Returns:
            bool: True if operator can be appended
        '''
        if not expression:
            return True
            
        last_char = expression[-1]

        if last_char in CalculatorConfig.OPERATORS or last_char in CalculatorConfig.SPECIAL_CHARS:
            return True

        if last_char.isdigit():
            return True
            
        return False
    
    @staticmethod
    def can_append_dot(expression):
        '''
        Checks if decimal point can be appended to expression.
        
        Args:
            expression (str): Current expression
            
        Returns:
            bool: True if dot can be appended
        '''
        if not expression:
            return True
            
        last_char = expression[-1]

        number_segments = re.split(r'[\+\-\×÷\(\)]', expression)      
        if last_char.isdigit() and '.' not in number_segments[-1]:
            return True
        elif last_char in CalculatorConfig.OPERATORS and '.' not in number_segments[-2]:
            if expression[-2] not in [')', '%']:
                return True
                
        return False


class ExpressionBuilder:
    '''Builds and modifies calculator expressions'''
    
    @staticmethod
    def normalize_number(number_string):
        '''
        Converts string representation to float.
        
        Args:
            number_string (str): String with possible parentheses
            
        Returns:
            float: Normalized number
        '''
        return float(number_string.strip('()'))
    
    @staticmethod
    def format_number(number):
        '''
        Formats number for display in expression.
        
        Args:
            number (float): Number to format
            
        Returns:
            str: Formatted number string
        '''
        if number.is_integer():
            return '({})'.format(int(number)) if number < 0 else str(int(number))
        return '({})'.format(number) if number < 0 else str(number)
    
    @staticmethod
    def append_digit_to_expression(expression, digit):
        '''
        Appends digit to expression with proper formatting.
        
        Args:
            expression (str): Current expression
            digit (str): Digit to append
            
        Returns:
            str: Updated expression
        '''
        if expression and expression[-1] == ')':
            return expression + '×' + digit
        return expression + digit
    
    @staticmethod
    def append_operator_to_expression(expression, operator):
        '''
        Appends operator to expression.
        
        Args:
            expression (str): Current expression
            operator (str): Operator to append
            
        Returns:
            str: Updated expression
        '''
        if not expression:
            return '0' + operator
            
        last_char = expression[-1]

        if last_char in CalculatorConfig.OPERATORS + ['.']:
            return expression[:-1] + operator
            
        return expression + operator


class CalculationState:
    '''Manages the state of calculator operations'''
    
    def __init__(self):
        self._expression = ''
        self._calculation_done = False
    
    @property
    def expression(self):
        '''Gets current expression'''
        return self._expression
    
    @property
    def is_calculation_done(self):
        '''Gets calculation completion status'''
        return self._calculation_done
    
    def set_expression(self, expression):
        '''
        Sets the current expression.
        
        Args:
            expression (str): New expression
        '''
        self._expression = expression
    
    def mark_calculation_done(self):
        '''Marks calculation as completed'''
        self._calculation_done = True
    
    def reset_calculation_state(self):
        '''Resets calculation completion flag'''
        self._calculation_done = False
    
    def clear_expression(self):
        '''Clears the current expression'''
        self._expression = ''


class ExpressionManager:
    '''Coordinates expression building, validation, and state management'''
    
    def __init__(self):
        self.state = CalculationState()
        self.builder = ExpressionBuilder()
        self.validator = InputValidator()
    
    def _return_change_result(self, has_changed, display_value = None):
        '''
        Returns standardized change result.
        
        Args:
            has_changed (bool): Whether expression changed
            display_value (str, optional): Value to display
            
        Returns:
            tuple: (has_changed, display_value)
        '''
        if display_value is not None:
            return (has_changed, CalculatorConfig.INITIAL_DISPLAY)
        return (has_changed, self.state.expression)
    
    def add_digit(self, digit):
        '''
        Adds digit to current expression.
        
        Args:
            digit (str): Digit to add
            
        Returns:
            tuple: (success: bool, updated_expression: str)
        '''
        try:
            if self.state.is_calculation_done:
                if digit == '0':
                    self.state.clear_expression()
                    self.state.reset_calculation_state()
                    return self._return_change_result(True, CalculatorConfig.INITIAL_DISPLAY)
                self.state.set_expression(digit)
                self.state.reset_calculation_state()
                return self._return_change_result(True)
            
            if not self.validator.can_append_digit(self.state.expression, digit):
                return self._return_change_result(False)
            
            updated_expression = self.builder.append_digit_to_expression(self.state.expression, digit)
            self.state.set_expression(updated_expression)
            return self._return_change_result(True)
            
        except Exception as e:
            return self._return_change_result(False)
    
    def add_operator(self, operator):
        '''
        Adds operator to current expression.
        
        Args:
            operator (str): Operator to add
            
        Returns:
            tuple: (success: bool, updated_expression: str)
        '''
        try:
            if self.state.is_calculation_done:
                self.state.reset_calculation_state()
            
            if not self.validator.can_append_operator(self.state.expression):
                return self._return_change_result(False)
            
            updated_expression = self.builder.append_operator_to_expression(self.state.expression, operator)
            self.state.set_expression(updated_expression)
            return self._return_change_result(True)
            
        except Exception as e:
            return self._return_change_result(False)
                
    def add_decimal_point(self):
        '''
        Adds decimal point to current expression.
        
        Returns:
            tuple: (success: bool, updated_expression: str)
        '''
        try:
            if self.state.is_calculation_done:
                self.state.set_expression('0.')
                self.state.reset_calculation_state()
                return self._return_change_result(True)
            
            if not self.state.expression:
                self.state.set_expression('0.')
                return self._return_change_result(True)
            
            if not self.validator.can_append_dot(self.state.expression):
                return self._return_change_result(False)
            
            last_char = self.state.expression[-1]

            if last_char.isdigit():
                self.state.set_expression(self.state.expression + '.')
                return self._return_change_result(True)
            elif last_char in CalculatorConfig.OPERATORS:
                if self.state.expression[-2] not in [')', '%']:
                    updated_expression = self.state.expression[:-1] + '.'
                    self.state.set_expression(updated_expression)
                    return self._return_change_result(True)
            
            return self._return_change_result(False)
            
        except Exception as e:
            return self._return_change_result(False)

    def toggle_sign(self):
        '''
        Toggles the sign of the last number in expression.
        
        Returns:
            tuple: (success: bool, updated_expression: str)
        '''
        try:
            if self.state.is_calculation_done:
                self.state.reset_calculation_state()
            
            match = re.search(r'(?:\d+(?:\.\d+)?|\(-\d+(?:\.\d+)?\)|\(\d+(?:\.\d+)?\))$', self.state.expression)
            if not match:
                return self._return_change_result(False)
            
            last_number_float = self.builder.normalize_number(match.group())
            if last_number_float == 0:
                return self._return_change_result(False)

            new_number = -last_number_float
            updated_expression = self.state.expression[:match.start()] + self.builder.format_number(new_number)
            self.state.set_expression(updated_expression)
            return self._return_change_result(True)
            
        except Exception as e:
            return self._return_change_result(False)

    def add_percent(self):
        '''
        Adds percent symbol to current expression.
        
        Returns:
            tuple: (success: bool, updated_expression: str)
        '''
        try:
            if self.state.is_calculation_done:
                self.state.reset_calculation_state()
            
            if not self.state.expression:
                return self._return_change_result(False)
            
            last_char = self.state.expression[-1]
            
            if last_char in CalculatorConfig.OPERATORS and self.state.expression[-2] == '%':
                return self._return_change_result(False)
            
            if last_char in CalculatorConfig.OPERATORS + ['%', '.']:
                updated_expression = self.state.expression[:-1] + '%'
                self.state.set_expression(updated_expression)
                return self._return_change_result(True)
            else:
                self.state.set_expression(self.state.expression + '%')
                return self._return_change_result(True)
                
        except Exception as e:
            return self._return_change_result(False)

    def clear_last_input(self):
        '''
        Clears the last input from expression.
        
        Returns:
            tuple: (success: bool, updated_expression: str)
        '''
        try:
            if self.state.is_calculation_done:
                self.state.clear_expression()
                self.state.reset_calculation_state()
                return self._return_change_result(True, CalculatorConfig.INITIAL_DISPLAY)
            
            if len(self.state.expression) <= 1:
                self.state.clear_expression()
                return self._return_change_result(True, CalculatorConfig.INITIAL_DISPLAY)
            
            if self.state.expression[-1] == ')':
                for i in range(len(self.state.expression) - 1, -1, -1):
                    if self.state.expression[i] == '(':
                        updated_expression = self.state.expression[:i] + self.state.expression[i + 2: -1]
                        self.state.set_expression(updated_expression)
                        break
                else:
                    return self._return_change_result(False)
                return self._return_change_result(True)
            
            if len(self.state.expression) == 2 and self.state.expression[0] == '0':
                self.state.clear_expression()
                return self._return_change_result(True, CalculatorConfig.INITIAL_DISPLAY)
            
            updated_expression = self.state.expression[:-1]
            self.state.set_expression(updated_expression)
            return self._return_change_result(True)
            
        except Exception as e:
            return self._return_change_result(False)

    def clear_all(self):
        '''
        Clears entire expression.
        
        Returns:
            tuple: (success: bool, updated_expression: str)
        '''
        try:
            if self.state.is_calculation_done:
                self.state.reset_calculation_state()
            
            if self.state.expression:
                self.state.clear_expression()
                return self._return_change_result(True, CalculatorConfig.INITIAL_DISPLAY)
            
            return self._return_change_result(False)
            
        except Exception as e:
            return self._return_change_result(False)


class ExpressionEvaluator:
    '''Handles mathematical evaluation of expressions'''
    
    @staticmethod
    def normalize_expression(expression):
        '''
        Normalizes expression for evaluation.
        
        Args:
            expression (str): Expression to normalize
            
        Returns:
            str: Normalized expression
        '''
        if expression[-1] in ('+', '-', '*', '/', '.'):
            expression = expression[:-1]
        return expression.replace('×', '*').replace('÷', '/')
    
    @staticmethod
    def format_result(result):
        '''
        Formats calculation result for display.
        
        Args:
            result: Calculation result
            
        Returns:
            str: Formatted result string
        '''
        if isinstance(result, str):
            return result
            
        try:
            result = float(result)
        except (ValueError, TypeError):
            return str(result)
        
        if result.is_integer():
            result_int = int(result)
            result_str = str(result_int)

            if len(result_str) > DisplayConfig.MAX_DISPLAY_LENGTH:
                return f'{result:.{DisplayConfig.SCIENTIFIC_PRECISION}e}'
            return result_str
        
        if abs(result) >= 1e12 or (abs(result) < 1e-6 and result != 0):
            return f'{result:.{DisplayConfig.SCIENTIFIC_PRECISION}e}'
        
        result_str = f'{result:.{DisplayConfig.DECIMAL_PLACES}f}'.rstrip('0').rstrip('.')
        
        if len(result_str) > DisplayConfig.MAX_DISPLAY_LENGTH:
            return f'{result:.{DisplayConfig.SCIENTIFIC_PRECISION}e}'
        
        return result_str
    
    @staticmethod
    def evaluate_expression(expression):
        '''
        Evaluates mathematical expression.
        
        Args:
            expression (str): Expression to evaluate
            
        Returns:
            str: Formatted result or error message
        '''
        if not expression:
            return ''
        
        try:
            expression = ExpressionEvaluator.normalize_expression(expression)
            
            if '%' not in expression:
                pass
            else:
                expression = ExpressionEvaluator._transform_percent_expression(expression)

            result = eval(expression)
            return ExpressionEvaluator.format_result(result)
            
        except Exception as e:
            return 'Error'

    @staticmethod
    def _transform_percent_expression(expression):
        '''
        Transforms percent operations in expression to regular mathematical operations.
        
        Args:
            expression (str): Expression with percent symbols
            
        Returns:
            str: Transformed expression without percent symbols
        '''
        # Find all tokens including numbers (with optional parentheses), operators, and parentheses
        tokens = re.findall(r'\(-?\d+(?:\.\d+)?\)%?|-?\d+(?:\.\d+)?%?|[+\-*/()]', expression)
        
        transformed_tokens = []
        prev_value = ''
        
        percent_numbers = [percent_number.replace('(', '').replace(')', '') for percent_number in re.findall(r'\(?-?\d+(?:\.\d+)?\)?%', expression)]
        for i, token in enumerate(tokens):
            if token.startswith('('):
                    token = token.replace('(', '').replace(')', '')
            if token.endswith('%'):
                number_part = token[:-1]
                
                prev_operator = None
                base_number = None
                
                for j in range(i - 1, -1, -1):
                    if tokens[j] in ['+', '-', '*', '/']:
                        prev_operator = tokens[j]

                        for k in range(j - 1, -1, -1):
                            if re.match(r'\(-?\d+(?:\.\d+)?\)|-?\d+(?:\.\d+)?', tokens[k]):
                                if prev_value != '':
                                    base_number = prev_value
                                else:
                                    base_number = tokens[k] 
                                break
                        break
                
                if prev_operator in ['+', '-'] and base_number:
                    current_value = f'({tokens[i - 2]}{prev_operator}({base_number}*{number_part}/100))'
                    transformed_tokens.append(f'({base_number}*{number_part}/100)')
                else:
                    current_value = f'({number_part}/100)'
                    transformed_tokens.append(f'({number_part}/100)')

                try:
                    if tokens[i + 2] in percent_numbers:
                        prev_value = current_value
                    else:
                        prev_value = ''
                except IndexError:
                    prev_value = ''

            else:
                transformed_tokens.append(token)

        return ''.join(transformed_tokens)

    
class CalculatorApp:
    '''Main calculator application GUI'''

    def __init__(self, root, expression_manager, evaluator):
        '''
        Initialize calculator application.
        
        Args:
            root: Tkinter root window
            expression_manager: Expression management instance
            evaluator: Expression evaluation instance
        '''
        self.root = root
        self.expression_manager = expression_manager
        self.evaluator = evaluator
        
        self._setup_window()
        self._create_labels()
        self._create_button_interface()

    def _setup_window(self):
        '''Configure main window properties'''
        self.root.title('Calculator')
        self.root.geometry('350x610')
        self.root.configure(bg = CalculatorConfig.BG_COLOR)
        self.root.resizable(False, False)

    def _create_labels(self):
        '''Create display and history labels'''
        self.display_label = self._design_label(
            CalculatorConfig.DISPLAY_FONT, 
            CalculatorConfig.INITIAL_DISPLAY
        )
        self.history_label = self._design_label(
            CalculatorConfig.HISTORY_FONT,
            CalculatorConfig.EMPTY_HISTORY,
            fg = '#AFAFAF',
            pady = (0, 10)
        )

    def _design_label(self, font, text = CalculatorConfig.INITIAL_DISPLAY, fg = CalculatorConfig.TEXT_COLOR, pady = (10, 0)):
        '''
        Create a styled label for the calculator.
        
        Args:
            font: Font configuration
            text (str): Initial text
            fg (str): Foreground color
            pady (tuple): Vertical padding
            
        Returns:
            tk.Label: Configured label widget
        '''
        label = tk.Label(
            self.root,
            borderwidth = 0,
            text = text,
            font = font,
            bg = CalculatorConfig.BG_COLOR,
            fg = fg,
            anchor = 'e',
            relief = 'sunken',
            pady = 3
        )
        label.pack(fill = 'x', padx = 15, pady = pady)
        return label

    def _create_button_interface(self):
        '''Create calculator button interface'''
        button_frame = tk.Frame(self.root, bg = CalculatorConfig.BG_COLOR)
        button_frame.pack(side = 'bottom', padx = 5, pady = 5)
        
        button_definitions = [
            (
                ('⟵', lambda: self._handle_clear_last()),
                ('⁺⁄₋', lambda: self._handle_toggle_sign()),
                ('%', lambda: self._handle_percent()),
                ('÷', lambda: self._handle_operator('÷'))
            ),
            (
                ('7', lambda: self._handle_digit('7')),
                ('8', lambda: self._handle_digit('8')),
                ('9', lambda: self._handle_digit('9')),
                ('×', lambda: self._handle_operator('×'))
            ),
            (
                ('4', lambda: self._handle_digit('4')),
                ('5', lambda: self._handle_digit('5')),
                ('6', lambda: self._handle_digit('6')),
                ('-', lambda: self._handle_operator('-'))
            ),
            (
                ('1', lambda: self._handle_digit('1')),
                ('2', lambda: self._handle_digit('2')),
                ('3', lambda: self._handle_digit('3')),
                ('+', lambda: self._handle_operator('+'))
            ),
            (
                ('⟸', lambda: self._handle_clear_all()),
                ('0', lambda: self._handle_digit('0')),
                ('.', lambda: self._handle_decimal_point()),
                ('=', lambda: self._handle_evaluate())
            )
        ]

        for row_index, row_buttons in enumerate(button_definitions):
            for column_index, (text, command) in enumerate(row_buttons):
                bg_color, bg_active = _get_button_colors(row_index, column_index)
                button = tk.Button(
                    button_frame,
                    text = text,
                    width = 2,
                    height = 1,
                    font = CalculatorConfig.BUTTON_FONT,
                    bg = bg_color,
                    fg = CalculatorConfig.TEXT_COLOR,
                    activebackground = bg_active,
                    activeforeground = CalculatorConfig.TEXT_COLOR_ACTIVE,
                    command = command
                )
                button.grid(row = row_index, column = column_index)

    def _handle_digit(self, digit):
        '''Handle digit button press'''
        success, updated_expression = self.expression_manager.add_digit(digit)
        if success:
            self._update_display(updated_expression)

    def _handle_operator(self, operator):
        '''Handle operator button press'''
        success, updated_expression = self.expression_manager.add_operator(operator)
        if success:    
            self._update_display(updated_expression)

    def _handle_decimal_point(self):
        '''Handle decimal point button press'''
        success, updated_expression = self.expression_manager.add_decimal_point()
        if success:
            self._update_display(updated_expression)

    def _handle_clear_last(self):
        '''Handle clear last input button press'''
        success, updated_expression = self.expression_manager.clear_last_input()
        if success:
            self._update_display(updated_expression)

    def _handle_clear_all(self):
        '''Handle clear all button press'''
        success, updated_expression = self.expression_manager.clear_all()
        if success:
            self._update_display(updated_expression)

    def _handle_toggle_sign(self):
        '''Handle toggle sign button press'''
        success, updated_expression = self.expression_manager.toggle_sign()
        if success:
            self._update_display(updated_expression)

    def _handle_percent(self):
        '''Handle percent button press'''
        success, updated_expression = self.expression_manager.add_percent()
        if success:
            self._update_display(updated_expression)

    def _handle_evaluate(self):
        '''Handle equals button press'''
        expression = self.expression_manager.state.expression
        result = self.evaluator.evaluate_expression(expression)

        if result and result == 'Error':
            self.expression_manager.state.mark_calculation_done()
            self.expression_manager.state.clear_expression()
            self._update_display('Error')
            return
        
        if result:
            self.expression_manager.state.mark_calculation_done()
            self._update_display(expression, result)
                
    def _update_display(self, expression, result = CalculatorConfig.EMPTY_HISTORY):
        '''
        Update calculator display labels.
        
        Args:
            expression (str): Current expression
            result (str): Calculation result
        '''
        if result != CalculatorConfig.EMPTY_HISTORY:
            self.display_label.config(text = result)
            self.history_label.config(text = expression)
            self.expression_manager.state.set_expression(result)
        else:       
            self.display_label.config(text = expression)
            self.history_label.config(text = result)