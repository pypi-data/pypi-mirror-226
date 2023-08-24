# Template.py - Advanced Terminal Styling for Django Templates

"""
The 'Template.py' module in your Django project enhances terminal-based styling and provides
tools to convert HTML content into Django template format. It introduces advanced terminal
size retrieval for more precise styling, and offers a function to seamlessly convert HTML
files into Django template format with static tag replacements.

Usage:
    This module is designed to be imported and used within your Django project for terminal-
    based styling enhancements and HTML-to-template conversion.

Features:
    - 't_size()': A function to retrieve advanced terminal dimensions for responsive styling.
    - 'convert_to_django_html(input_file, output_file)': Convert HTML files to Django
      template format by replacing 'href' and 'src' attributes with Django static tags.
    - 'djangotemp()': Converts HTML files in the current directory to Django template format,
      saving them in an 'output_html_files' directory.

Functions:
    - 't_size()': Retrieve advanced terminal dimensions for precise styling in templates.
    - 'convert_to_django_html(input_file, output_file)': Convert HTML to Django template
      format with static tag replacements.
    - 'djangotemp()': Batch convert HTML files to Django template format in the current
      directory.

"""

import re, os
from Designer.BackGroundColor import *
from Designer.ForeGroundColor import *

def t_size():
    """
    Retrieve the current terminal size in columns (width) and lines (height).

    This function utilizes the 'os.get_terminal_size()' method to obtain the dimensions
    of the current terminal window. It returns a list containing the terminal width and height.

    Returns:
        list: A list containing the terminal width (columns) and height (lines).
    """
    terminal_size = os.get_terminal_size()
    terminal_width = terminal_size.columns
    terminal_height = terminal_size.lines
    return [terminal_width, terminal_height]


def convert_to_django_html(input_file, output_file):
    """
    Convert HTML file to Django template format with static tag replacements.

    This function reads the content of an HTML file and converts the 'href' and 'src'
    attributes to Django static tags, making it compatible with Django templates.

    Args:
        input_file (str): Path to the input HTML file.
        output_file (str): Path to the output Django template file.

    """
    with open(input_file, 'r') as f:
        html_content = f.read()

    # Use regular expressions to find all href and src attributes
    href_pattern = r'href="((?!https:|{% static ).+?)"'
    src_pattern = r'src="((?!https:|{% static ).+?)"'

    # Convert href attributes to Django static tags
    django_html_content = re.sub(href_pattern, r'''href="{% static '\1' %}"''', html_content)

    # Convert src attributes to Django static tags, skipping if already in the format {% static '' %}
    django_html_content = re.sub(src_pattern, r'''src="{% static '\1' %}"''', django_html_content)

    with open(output_file, 'w') as f:
        f.write(django_html_content)

def djangotemp():
    """
    Convert HTML files in the current directory to Django template format.

    This function searches for HTML files in the current directory and converts them to
    Django template format by replacing 'href' and 'src' attributes with Django static tags.
    The converted files are saved in a separate 'output_html_files' directory.

    """
    input_directory = os.getcwd()
    output_directory = "output_html_files"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get the list of file names in the input directory
    file_names = os.listdir(input_directory)

    # Loop through each file in the input directory
    
    for file_name in file_names:
        if file_name.endswith(".html"):
            input_file_path = os.path.join(input_directory, file_name)
            output_file_path = os.path.join(output_directory, file_name)
            convert_to_django_html(input_file_path, output_file_path)
            print("The "+yellow(file_name)+" template are converted into django template - "+green("OK"))

    print(grey(f"Conversion completed. Django HTML files are saved in the {blue('output_html_files')} directory.")+" - "+green("OK"))
