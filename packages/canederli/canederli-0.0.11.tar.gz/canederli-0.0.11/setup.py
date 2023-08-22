
from setuptools import setup, find_packages

VERSION = '0.0.11' 

DESCRIPTION = 'Simple tools to quickly get the names of multiple variables out of the lines of code where they are defined.'

LONG_DESCRIPTION = \
"""
This package contains the function 'canederlist' 

i.e. 

Comma 
And 
NEwline 
Delimited 
Elements 
Reformatted as 
LIst of 
STrings 

which allows to reformat a multiline string containing words separated by commas into a list of strings.

This is useful when we have a list of variables and we want to quickly get a list of their names as strings.


usage
-----

The list of variables (i.e. not the variable containing the list, the hardcoded list of variables) must be copied and pasted as argument of canederlist(), enclosed in triple quotes (\"\"\").

The function canederlist will remove 
 - multiple spaces (double or more, but not single spaces)
 - newline characters
 - triple points ...
 - (if selected in the input) round () and square [] parentheses
 - (if selected in the input) single spaces
and split the remaining elements separated by commas into a list of strings.


example
-------

>>>from canederli import canederlist
>>>columns = [ names, 
            descriptions, 
            x_coordinates, 
            y_coordinates ]

>>>columns_labels = canederlist(\"\"\"
 names, 
            descriptions, 
            x_coordinates, 
            y_coordinates 
\"\"\")

>>>print(columns_labels)
['names', 'descriptions', 'x_coordinates', 'y_coordinates']


example removing parentheses
----------------------------


>>>from canederli import canederlist
>>>columns = [ names, 
            descriptions, 
            x_coordinates, 
            y_coordinates ]

>>>columns_labels = canederlist(\"\"\"
 names, 
            descriptions, 
            x_coordinates, 
            y_coordinates 
\"\"\",1)  # <--- this is like setting optional parameter rm_parentheses=False

>>>print(columns_labels)
['names', 'descriptions', 'x_coordinates', 'y_coordinates']

"""

setup(
        name="canederli", 
        version=VERSION,
        author="tms1991",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',  # added to avoid any special character in LONG_DESCRIPTION raises errors in PyPi server
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['multiline', 'strings', 'list', 'variables', 'names', 'labels'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

