import sys
import os
import os.path
from IPython.display import display, HTML, Latex, Javascript
from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)
from pygments import highlight
from pygments.lexers import TexLexer
from pygments.formatters import HtmlFormatter

class mwe(object):
    """ ``mwe`` initializes a minimum working example for LaTeX.

    ``mwe`` starts a latex document with changeable class, options, and premble.
    The text is then passed into the body of the document.

    :param text: Valid LaTeX source code (be careful of escape characters)
    :param texcls: LaTeX class name, default 'article'
    :param texclsopts: LaTeX options passed to the LaTeX class, as a dict.  For
        keyword arguments, use {"keyword": "arg"}, and for singular
        arguments, use {"argument": None}.
    :param preamble: Valid LaTeX source code
    :returns: An ``mwe`` object for additional editing or exporting.
    """
    def __init__(self, text=None,
                 texcls="article", texclsopts={"letterpaper": None},
                 preamble=None):
        self.preamble = \
            """%% preamble here \n"""
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
        self.export()
        if alone:
            self.show_alone()
        else:
            self.show_side_by_side()

    def show_alone(self):
        """ some docstring here. """

    def export(self):
        """ some docstring here. """
        tex_str = ''
        optstr = 'letterpaper'
        tex_str += "\documentclass[%s]{%s}\n" % (optstr, self.texcls)
        tex_str += "%s\n" % self.preamble
        tex_str += "\\begin{document}\n"
        tex_str += self.body + "\n"
        tex_str += "\end{document}\n"
        self.tex_str = tex_str
        with open("/tmp/mwe.tex", 'w') as f:
            f.write(tex_str)
        f.close()
        cwd = os.getcwd()
        cmdstr = "pdflatex /tmp/mwe.tex --output-dir=%s" % cwd
        #print cmdstr
        os.system(cmdstr)
        cmdstr = "pdf2svg mwe.pdf mwe.svg"
        #print cmdstr
        os.system(cmdstr)
        os.system('rm -f mwe.aux mwe.log')

    def show_side_by_side(self):
        """ some docstring here. """
        with open("mwe.svg", 'r') as f:
            svgstr = f.read()
        f.close()
        formatted_tex_str = highlight(self.tex_str, TexLexer(), HtmlFormatter())
        htmlstr = \
            """
              <style>
                %s
              </style>
              <div style='float:left; width:45%%'>
                <pre>
                    %s
                </pre>
              </div>
              <div style='float:right; width:45%%; border: solid 1px black;'>
                %s
              </div>""" % (HtmlFormatter().get_style_defs('.highlight'), formatted_tex_str, svgstr)
        return display(HTML(htmlstr))

"""
@register_cell_magic
def mwe(line, cell):
    " Some docstring here "
    # process class and class options from linemagic
    # Now make the mwe
    currentmwe = mwe(cell, texcls, texclsopts, preamble)
    # Now show side by side
    mwe.show()
    return line, cell
"""
