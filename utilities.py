from config import CalculatorConfig


def _get_button_colors(row, column):
    '''
    Get button colors based on position.
        
    Args:
        row (int): Button row
        column (int): Button column
            
    Returns:
        tuple: (normal_color, active_color)
    '''
    if row != 0 and column != 3:
        return CalculatorConfig.BUTTON_COLOR_1, CalculatorConfig.BUTTON_COLOR_ACTIVE_1
    elif column == 3:
        return CalculatorConfig.BUTTON_OPERATOR_COLOR, CalculatorConfig.BUTTON_OPERATOR_COLOR_ACTIVE
    else:
        return CalculatorConfig.BUTTON_COLOR_2, CalculatorConfig.BUTTON_COLOR_ACTIVE_2