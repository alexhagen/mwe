import sys
import os
from IPython.display import display, HTML, Latex, Javascript
from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

class mwe(object):
    """ Some docstring here """
    def __init__(self, text=None, texcls="article", texclsopts={}, preamble=None):
        self.preamble = \
            """ preamble here """
        if preamble is not None:
            self.preamble += preamble
        self.texcls = texcls
        self.texclsopts = texclsopts
        self.body = ""
        if text is not None:
            self.add_to_body(text)

    def add_to_body(self, text):
        self.body += text

    def show(self, alone=False):
        """ some docstring here. """
        if alone:
            self.show_alone()
        else:
            self.show_side_by_side()

    def show_alone(self):
        """ some docstring here. """

    def export(self):
        """ some docstring here. """

    def show_side_by_side(self):
        """ some docstring here. """
        htmlstr = "<div></div><div></div>"
        return display(HTML(htmlstr))

@register_cell_magic
def mwe(line, cell):
    """ Some docstring here """
    # process class and class options from linemagic
    # Now make the mwe
    currentmwe = mwe(cell, texcls, texclsopts, preamble)
    # Now show side by side
    mwe.show()
    return line, cell
