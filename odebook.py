# Copyright (c) 2016 Ilya V. Schurov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import matplotlib.pyplot as plt

cf = None
# cf stands for 'current figure', it is the name of current figure
# to use in allsave, labels and so on
# it is modified with needfigure

def needfigure(basename, ext='exists', prefix='fig'):
    """
    Checks whether figure with name <basename> already created or no.
    Returns False if there exists file ._<basename>_exists (or ._<basename>_<ext>,
    if the latter is given) in the appropriate figure dir.
    Returns True and creates <basename>.exists if it does not exists

    Also sets cf global to <basename>.
    """

    global cf
    cf = basename

    filename = os.path.join(prefix, "._" + basename) + "_" + ext
    if os.path.exists(filename):
        return False
    else:
        with open(filename,'w'):
            pass
        return True


def savefigs(basename=None, exts=("svg", "pdf"), prefix="fig", tight_layout=True):
    if basename is None:
        basename = cf
    if tight_layout:
        plt.tight_layout()
    for ext in exts:
        plt.savefig(os.path.join(prefix, basename) + "." + ext)

def mkfig(title="", width='responsive', frac=0.9, basename=None, prefix="fig"):
    if basename is None:
        basename = cf
    filename = os.path.join(prefix, basename)
    return u"FIGURE: [{filename}, width={width} frac={frac}] {title} label{{fig:{basename}}}".format(title=title, width=width, frac=frac, filename=filename, basename=basename)

