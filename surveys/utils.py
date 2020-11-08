import ast

def string_to_list(string) -> list:
    """
    Conversting string to list
    '[1,2,3]' -> [1,2,3]
    '1;2;3;' -> [1,2,3]
    """
    try:
        data = ast.literal_eval(string)
        assert isinstance(data, list), 'Data shoud be in form of list'
    except SyntaxError:
        data = list(filter(lambda x: x, map(str.strip, string.split(';'))))
    return data