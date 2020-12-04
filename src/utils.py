
def convert_to_decimal_notation(c, separator):
    if c.isdigit():
        return c
    elif c == separator:
        return '.'
    else:
        return ''


def float_from_currency_str(s, separator):
    # separator is decimal point notation, either '.' or ','
    value_as_list = [convert_to_decimal_notation(
        c, separator) for i, c in enumerate(s)]
    return float(''.join(value_as_list))
