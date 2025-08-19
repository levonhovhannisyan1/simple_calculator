class DisplayConfig:
    '''Configuration constants for display formatting'''
    MAX_DISPLAY_LENGTH = 12
    SCIENTIFIC_PRECISION = 6
    DECIMAL_PLACES = 10


class CalculatorConfig:
    '''Configuration constants for calculator behavior'''
    OPERATORS = ['+', '-', '×', '÷']
    SPECIAL_CHARS = ['%', '.', ')', '(']
    INITIAL_DISPLAY = '0'
    EMPTY_HISTORY = ''
    
    # UI Constants
    BG_COLOR = '#1C1C1C'
    BUTTON_COLOR_1 = '#505050'
    BUTTON_COLOR_ACTIVE_1 = '#6B6B6B'
    BUTTON_COLOR_2 = '#B1B1B1'
    BUTTON_COLOR_ACTIVE_2 = '#C7C7C7'
    BUTTON_OPERATOR_COLOR = '#FF9500'
    BUTTON_OPERATOR_COLOR_ACTIVE = '#FFB855'
    TEXT_COLOR = '#FFFFFF'
    TEXT_COLOR_ACTIVE = '#F1EFEF'
    
    DISPLAY_FONT = ('Arial', 35)
    HISTORY_FONT = ('Arial', 20)
    BUTTON_FONT = ('Ani', 35)