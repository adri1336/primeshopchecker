def xpath_find_elements_by_text(element, search_strings):
    uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
    xpath_conditions = [
        f"contains(translate(text(), '{uppercase_letters}', '{
            lowercase_letters}'), '{search.lower()}')"
        for search in search_strings
    ]
    xpath_expression = f"//{element}[{' or '.join(xpath_conditions)}]"
    return xpath_expression


def xpath_find_elements_by_class(element, search_strings):
    xpath_conditions = [
        f"contains(@class, '{search}')"
        for search in search_strings
    ]
    xpath_expression = f"//{element}[{' or '.join(xpath_conditions)}]"
    return xpath_expression


def xpath_find_elements_by_partial_id(element, search_strings):
    xpath_conditions = [
        f"contains(@id, '{search}')"
        for search in search_strings
    ]
    xpath_expression = f"//{element}[{' or '.join(xpath_conditions)}]"
    return xpath_expression
