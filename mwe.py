from __future__ import print_function
import sys
import os
import os.path
from IPython.display import display, HTML, Latex, Javascript
from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)
from pygments import highlight
from pygments.lexers import TexLexer
from pygments.formatters import HtmlFormatter
import itertools
import numpy as np

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
    __counter__ = itertools.count()
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
        self.__number__ = next(self.__counter__)

    def add_to_body(self, text):
        """ adds valid LaTeX source into the body

            :param text: valid LaTeX source to add to the end of the current
                document body text.
        """
        self.body += '\n' + text + '\n'
        return self

    def show(self, alone=False, **kwargs):
        """ exports and shows the result of the mwe.

        ``show`` will export the LaTeX ``mwe`` into an svg and show it below in
        the Jupyter notebook.

        :param alone: Whether to show **only** the result (``True``), or show it
            side by side with the LaTeX source (``False``).  Default ``False``.
        """
        self.export(**kwargs)
        if alone:
            self.show_alone()
        else:
            self.show_side_by_side()
        return self

    def show_alone(self):
        """ some docstring here. """
        with open("%s.svg" % self.filename, 'r') as f:
            svgstr = f.read()
        f.close()
        htmlstr = \
            """
              <div style='width:80%%; border: solid 1px black;'>
                <img src='data:image/svg+xml;charset=UTF-8,%s' width="100%%"/>
              </div>""" % (svgstr)
        self.__number__ = next(self.__counter__)
        htmlstr = \
            """
              <div style='width:80%%; border: solid 1px black;'>
                <img src='%s' width="100%%"/>
              </div>""" % ("%s.svg?%d" % (self.filename, self.__number__))
        return display(HTML(htmlstr))

    def export(self, filename='mwe', engine='pdflatex', options='',
               steps=[], interaction=''):
        """Compiles the LaTeX into an ``.svg``

        ``export`` calls ``pdflatex`` to convert the ``mwe`` into a ``.pdf``
        and then uses ``pdf2svg`` to convert this into an svg. The LaTeX source
        is written into the ``/tmp`` directory, but the ``mwe.pdf`` and
        ``mwe.svg`` files will be compiled in the current directory.

        inputs:
            - filename:
            - engine:
            - options:
            - steps:
            - interaction:
        """
        self.filename = filename
        tex_str = ''
        optstr = ''
        for key, val in self.texclsopts.items():
            if val is None:
                optstr += '%s,' % key
            else:
                optstr += '%s=%s,' % (key, val)
        optstr = optstr[:-1]
        tex_str += "\documentclass[%s]{%s}\n" % (optstr, self.texcls)
        tex_str += "%s\n" % self.preamble
        tex_str += "\\begin{document}\n"
        tex_str += self.body + "\n"
        tex_str += "\end{document}\n"
        self.tex_str = tex_str
        with open("/tmp/%s.tex" % filename, 'w') as f:
            f.write(tex_str)
        f.close()
        cwd = os.getcwd()
        cmdstr = "%s %s %s /tmp/%s.tex --output-dir=%s" \
            % (engine, options, interaction, filename, cwd)
        os.system(cmdstr)
        for step in steps:
            print (step)
            os.system(step)
        cmdstr = "pdf2svg %s.pdf %s.svg" % (filename, filename)
        #cmdstr = 'inkscape --without-gui --file {pdf_file}.pdf --export-text-to-path --export-plain-svg={svg_file}.svg'.format(pdf_file=filename, svg_file=filename)
        #print (cmdstr)
        os.system(cmdstr)
        #os.system('rm -f %s.aux %s.log' % (filename, filename))
        return self

    def show_side_by_side(self):
        """ shows the source code and the result of the ``mwe``

        ``show_side_by_side`` exports the ``mwe`` into an ``.svg``, and then
        shows it in the Jupyter notebook as a side-by-side of the source code,
        highlighted with Pygments, and the ``.svg`` resulting page."""
        svgstr = "%s.svg?id=%d" % (self.filename, np.random.randint(0, 1e9))
        formatted_tex_str = highlight(self.tex_str, TexLexer(), HtmlFormatter())
        htmlstr = \
            """
              <style>
                %s
              </style>
	      <div style='float: left; width:100%%'>
              <div style='float:left; width:49%%'>
                <pre>
                    %s
                </pre>
              </div>
              <div style='float:right; width:49%%; border: solid 1px black;'>
                <img src='%s' width="100%%"/>
              </div>
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
