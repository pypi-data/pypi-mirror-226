import re

def canederlist(multiline_string: str, rm_parentheses=False, rm_spaces=False):

    # C comma
    # A and
    # N NEwline
    # E 
    # D delimited
    # E elements
    # R reformatted as
    # L LIst of
    # I
    # S
    # T STrings

    """example
-------

>>>columns_labels = canederlist(\"\"\"
 names, 
            descriptions, 
            x_coordinates, 
            y_coordinates 
\"\"\")

>>>print(columns_labels)

['names', 'descriptions', 'x_coordinates', 'y_coordinates']
"""

    if rm_spaces:
        multiline_string = multiline_string.replace(" ", "")
    else:        
        while "  " in multiline_string:
            multiline_string = multiline_string.replace("  ", " ")

    if rm_parentheses:
        multiline_string = multiline_string.replace("[", "")
        multiline_string = multiline_string.replace("]", "")
        multiline_string = multiline_string.replace("(", "")
        multiline_string = multiline_string.replace(")", "")

    multiline_string = multiline_string.replace("...", "")


    multiline_string = re.sub("\n", "", multiline_string)

    list_of_strings = multiline_string.split(",")

    list_of_strings = [ element.strip() for element in list_of_strings ]

    return list_of_strings