#!/usr/bin/python

"""
Creates the CSS files for Pelican.
There are a few things it needs to do:

     - Remove the .hll from the very first line

     - For each line, prepend it with a div.highlight > 

You have to have pygments installed on your machine before this works.
Check this by typing ``pygmentize`` in your terminal.
"""

import subprocess
from pygments.styles import get_all_styles, get_style_by_name

def get_theme_names():
    """
    Gets all the themes that are loaded.
    """
    return list(get_all_styles())

def write_css_files(theme_names):
    """
    Writes all the CSS files based on the theme names.
    Uses the output from pygmentize and edits it so it is compatible with
    Pelican.
    """

    def edit_row(row):
        """
        Edits each row, predending it with div.highlight > pre and removing
        .hll from the start of a row if it contains it.
        """
        row = "div.highlight > pre > " + row
        row = row + "\n"
        return row

    for theme_name in theme_names:
        outfile = open("%s.css" % theme_name, "wb")
        
        # the first row gives the background colour of the div. This is found
        # using the pygments library.
        theme = get_style_by_name(theme_name)
        outfile.write("div.highlight > pre { background-color : %s; }\n" %
                theme.background_color)

        # call the pygmentize script and grab the output.
        output = subprocess.check_output(["pygmentize", 
                                         "-S", 
                                         theme_name, 
                                         "-f",
                                         "html"])
        output = output.split("\n")[:-1]
        output = [edit_row(row)
                  for row in output]
        outfile.writelines(output)
        outfile.close()

if __name__ == "__main__":
    theme_names = get_theme_names()
    write_css_files(theme_names)
