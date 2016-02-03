#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Automatically generated file for compiling doconce documents.
"""
import sys, glob, os, shutil, subprocess, codecs, re

logfile = 'tmp_output.log'  # store all output of all operating system commands
f = open(logfile, 'w'); f.close()  # touch logfile so it can be appended

unix_command_recorder = []

def os_system(cmd):
    """Run system command cmd using the simple os.system command."""
    print cmd
    failure = os.system(cmd)
    if failure:
        print """Command
  %s
failed""" % cmd
        sys.exit(1)
    unix_command_recorder.append(cmd)  # record command for bash script

def system(cmd):
    """Run system command cmd using subprocess module."""
    print cmd
    try:
        output = subprocess.check_output(cmd, shell=True,
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print """Command
  %s
failed""" % cmd
        print 'Return code:', e.returncode
        print e.output
        print("Hello")
        sys.exit(1)
    print output
    f = open(logfile, 'a'); f.write(output); f.close()
    unix_command_recorder.append(cmd)  # record command for bash script
    return output

def spellcheck():
    for filename in glob.glob('*.do.txt'):
        if not filename.startswith('tmp'):
            cmd = 'doconce spellcheck -d .dict4spell.txt %(filename)s' % vars()
            system(cmd)

def latex(name,
          latex_program='pdflatex',    # or 'latex'
          options='--latex_code_style=vrb',
          version='paper',             # or 'screen', '2up', 'A4', 'A4-2up'
          postfix='',                  # or 'auto'
          ptex2tex=None,               # only for ptex2tex step
          ):
    """
    Make latex/pdflatex (according to latex_program) PDF file from
    the doconce file name (without any .do.txt extension).

    version can take the following values:

      * paper: normal page size, --device=paper
      * 2up: normal page size, --device=paper, 2 pages per sheet
      * A4: A4 page size, --device=paper
      * A4-2up: A4 page size, --device=paper, 2 pages per sheet
      * screen: normal pages size, --device=screen

    If a separate ptex2tex step is wanted, fill in all necessary
    commands in the ptex2tex string.
    """
    if name.endswith('.do.txt'):
        name = name.replace('.do.txt', '')
    system('rm -f %(name)s.aux' % vars())

    if version in ('paper', 'A4', '2up', 'A4-2up'):
        if not '--device=paper' in options:
            options += ' --device=paper'
    elif version == 'screen' and '--device=paper' in options:
        options = options.replace('--device=paper', '')
    if version in ('A4', 'A4-2up'):
        if not '--latex_papersize=a4' in options:
            options += ' --latex_papersize=a4'
    if postfix == 'auto':
        if version == 'paper':
            postfix = '4print'
        elif version == 'screen':
            postfix = '4screen'
        else:
            postfix = version

    # Compile source
    cmd = 'doconce format %(latex_program)s %(name)s %(options)s ' % vars()
    system(cmd)

    cmd = r"doconce replace '%% insert custom LaTeX commands...' '\usepackage[russian]{babel} \usepackage{titlesec} \titleformat{\subsubsection}[runin] {\normalfont\normalsize\bfseries}{\thesubsubsection.}{1em}{} \let\paragraph=\subsubsection' %(name)s.tex" % vars()
    system(cmd)

    cmd = r"doconce replace '\usepackage{lmodern}' '%%\usepackage{lmodern}' %(name)s.tex" % vars()
    system(cmd)
    # Transform .p.tex to .tex?
    if ptex2tex is not None:
        cmd = ptex2tex
        system(cmd)

    # Load latex file into string for examination
    dofile = open(name + '.tex', 'r')
    text = dofile.read()
    dofile.close()

    latex_options = ''
    if latex_program == 'pdflatex':
        latex_options = '-file-line-error -interaction nonstopmode -halt-on-error'

    # Run latex
    shell_escape = ' -shell-escape' if 'begin{minted}' in text else ''
    cmd_latex = '%(latex_program)s%(shell_escape)s %(latex_options)s %(name)s' % vars()
    system(cmd_latex)

    if 'idx{' in text:
        cmd = 'makeindex %(name)s' % vars()
        system(cmd)

    if 'BIBFILE:' in text:
        cmd = 'bibtex %(name)s' % vars()
        system(cmd)
    system(cmd_latex)
    system(cmd_latex)
    if latex_program == 'latex':
        cmd = 'dvipdf %(name)s' % vars()
        system(cmd)
        # Could instead of dvipdf run the old-fashioned dvips and ps2pdf

    if version in ('2up', 'A4-2up'):
        # Use pdfnup to make two pages per sheet
        cmd = 'pdfnup --frame true --outfile %(name)s.pdf %(name)s.pdf' % vars()
        system(cmd)
    if postfix:
        shutil.copy(name + '.pdf', name + '-' + postfix + '.pdf')


def html(name, options='', split=False):
    """
    Make HTML file from the doconce file `name`
    (without any .do.txt extension).
    """
    if name.endswith('.do.txt'):
        name = name.replace('.do.txt', '')

    # Compile source
    cmd = 'doconce format html %(name)s %(options)s ' % vars()
    system(cmd)


    cmd = u"doconce replace 'Figure' 'Рис.' %(name)s.html".encode('utf-8') % vars()
    system(cmd)

    cmd = u"doconce replace 'figure' 'рис.' %(name)s.html".encode('utf-8') % vars()
    system(cmd)

    cmd = u"doconce replace 'width=responsive' 'class=\"img-responsive\" style=\"max-width:600px; width:100%%;\"' %(name)s.html".encode('utf-8') % vars()
    system(cmd)

    if split:
        cmd = 'doconce split_html %(name)s' % vars()
        system(cmd)
        
        for filename in glob.glob("._%(name)s*.html" % vars()):
            if '000' not in filename:
                cmd = u"doconce replace '&larr; Prev' '&larr; Предыдущая глава' %s".encode('utf-8') % filename
                system(cmd)

                cmd = u"doconce replace 'Next &rarr;' ' Следующая глава &rarr;' %s".encode('utf-8') % filename
                system(cmd)

        for filename in [name, '._%s000' % name]:
            print(filename)
            cmd = u"doconce replace 'Read' 'Перейти к первой главе' %s.html".encode('utf-8') % filename 
            system(cmd)

            cmd = u"doconce subst '.*Next.*' '' %s.html".encode('utf-8') % filename 
            system(cmd)




def reveal_slides(name, options='', postfix='reveal', theme='darkgray'):
    """Make reveal.js HTML5 slides from the doconce file `name`."""
    if name.endswith('.do.txt'):
        name = name.replace('.do.txt', '')

    # Compile source
    if '--pygments_html_style=' not in options:
        from doconce.misc import recommended_html_styles_and_pygment_styles
        combinations = recommended_html_styles_and_pygment_styles()
        options += ' --pygments_html_style=%s' % combinations['reveal'][theme][0]
    if '--keep_pygments_html_bg' not in options:
        options += ' --keep_pygments_html_bg'
    options += ' --html_output="%(name)s-%(postfi)s'

    cmd = 'doconce format html %(name)s %(options)s ' % vars()
    system(cmd)

    cmd = 'doconce slides_html %(name)s-%(postfi)s reveal --html_slide_theme=%(theme)s'
    system(cmd)

def deck_slides(name, options='', postfix='deck', theme='sandstone.default'):
    """Make deck.js HTML5 slides from the doconce file `name`."""
    if name.endswith('.do.txt'):
        name = name.replace('.do.txt', '')

    # Compile source
    if '--pygments_html_style=' not in options:
        from doconce.misc import recommended_html_styles_and_pygment_styles
        combinations = recommended_html_styles_and_pygment_styles()
        options += ' --pygments_html_style=%s' % combinations['deck'][theme][0]
    if '--keep_pygments_html_bg' not in options:
        options += ' --keep_pygments_html_bg'
    options += ' --html_output="%(name)s-%(postfi)s'

    cmd = 'doconce format html %(name)s %(options)s ' % vars()
    system(cmd)

    cmd = 'doconce slides_html %(name)s-%(postfi)s deck --html_slide_theme=%(theme)s'
    system(cmd)

def beamer_slides(name, options='', postfix='beamer', theme='red_shadow',
                  ptex2tex_envir='minted'):
    """Make latex beamer slides from the doconce file `name`."""
    if name.endswith('.do.txt'):
        name = name.replace('.do.txt', '')
    system('rm -f %(name)s.aux' % vars())

    # Compile source
    shell_escape = '-shell-escape' if ptex2tex_envir == 'minted' else ''
    cmd = 'doconce format pdflatex %(name)s %(options)s ' % vars()
    system(cmd)
    # Run latex
    cmd = 'doconce ptex2tex %(name)s envir=%(ptex2tex_envir)s' % vars()
    system(cmd)
    cmd = 'doconce slides_beamer %(name)s --beamer_slide_theme=%(theme)s' % vars()
    system(cmd)
    cmd = 'pdflatex %(shell_escape)s %(name)s'
    system(cmd)
    system(cmd)
    system('cp %(name)s.pdf %(name)s-%(postfi).pdf' % vars())

    cmd = 'doconce slides_html %(name)s-%(postfi)s deck --html_slide_theme=%(theme)s'
    system(cmd)


def sphinx(name, options='', dirname='sphinx-rootdir',
           theme='pyramid', automake_sphinx_options='',
           split=False):
    """
    Make Sphinx HTML subdirectory from the doconce file `name`
    (without any .do.txt extension).
    """
    if name.endswith('.do.txt'):
        name = name.replace('.do.txt', '')

    if name.endswith('.do'):
        name = name.replace('.do','')

    # Compile source
    cmd = 'doconce format sphinx %(name)s %(options)s ' % vars()
    system(cmd)

    if split:
        cmd = 'doconce split_rst %(name)s' % vars()

    # Create sphinx directory
    cmd = 'doconce sphinx_dir theme=%(theme)s %(name)s' % vars()
    system(cmd)

    # Compile sphinx
    cmd = 'python automake_sphinx.py %(automake_sphinx_options)s' % vars()
    system(cmd)

def doconce2format(name, format, options=''):
    """Make given format from the doconce file `name`."""
    if name.endswith('.do.txt'):
        name = name.replace('.do.txt', '')

    # Compile source
    cmd = 'doconce format %(format)s %(name)s %(options)s ' % vars()
    system(cmd)

def plain(name, options=''):
    doconce2format(name, 'plain', options)

def pandoc(name, options=''):
    doconce2format(name, 'pandoc', options)

def ipynb(name, options=''):
    doconce2format(name, 'ipynb', options)

def cwiki(name, options=''):
    doconce2format(name, 'cwiki', options)

def mwiki(name, options=''):
    doconce2format(name, 'mwiki', options)

def gwiki(name, options=''):
    doconce2format(name, 'gwiki', options)

def cleanup_html(fn):
    show = False
    out = []
    with codecs.open(fn, "r", encoding='utf-8') as f:
        for line in f:
            if "<!-- ------------------- end of main content --------------- -->" in line:
                show = False
            if show:
                out.append(line)
            if "<!-- ------------------- main content ---------------------- -->" in line:
                show = True
    assert out, "No output in %s" % fn
    with codecs.open(fn, 'w', encoding='utf-8') as f:
        f.write("".join(out))

def mksnippets():
    for fn in glob.glob("._*.html"):
        with codecs.open(fn, 'r', encoding='utf-8') as thebook:
            snippet_name = None
            snippet_content = []
            snippets = {}
            for line in thebook:
                if 'navigation buttons at the bottom of the page' in line \
                        or 'end of snippets' in line:
                    break
                if 'snippet: ' in line:
                    m = re.search(ur'snippet:\s*(\w+)', line)
                    if m:
                        snippet_name = m.groups(1)
                        snippets[snippet_name] = snippet_content
                else:
                    if snippet_name:
                        if re.match('<h\d', line):
                            snippet_content = []
                            snippet_name = None
                        else:
                            snippet_content.append(line)

    for snippet_name, snippet_content in snippets.items():
        with codecs.open("snippets/%s.html" % snippet_name, 
                'w', encoding='utf-8') as snippet:
            snippet.write("".join(snippet_content))


def main():
    """
    Produce various formats from the doconce source.
    """

    dofile = "thebook"

    #spellcheck()

    common_options = '--encoding=utf-8 --examples_as_exercises '

    # --- HTML ---

    common_html_options = ' '

    # HTML Bootstrap
    bootstrap_options = ' --html_style=bootswatch_readable --html_code_style=inherit --html_pre_style=inherit --toc_depth=2 --pygments_html_style=default --html_template=template_bootstrap_wtoc.html --html_figure_caption=bottom --html_figure_hrule=top+bottom' 

    html(
      dofile,
      options=common_options + common_html_options + bootstrap_options,
      split=True)

    # One long HTML file
    #html(dofile, options=common_options + common_html_options + ' --html_style=bloodish --html_output=%s-1' % dofile, split=False)

    # Solarized HTML
    #html(dofile, options=common_options + common_html_options + ' --html_style=solarized3 --html_output=%s-solarized' % dofile, split=True)

    mksnippets()
    sys.exit(1)

    # --- latex ---

    common_latex_options = ' --latex_code_style=vrb'

    for version in 'paper', 'screen':  # , 'A4', '2up', 'A4-2up':
        latex(
          dofile,
          latex_program='pdflatex',
          options=common_options + common_latex_options,
          version=version,
          postfix='auto')

    # --- Sphinx ---

#    sphinx_themes = ['pyramid',]
#    for theme in sphinx_themes:
#        dirname = 'sphinx-rootdir' if len(sphinx_themes) == 1 else 'sphinx-rootdir-%s' % theme
#        sphinx(
#          dofile,
#          options=common_options + '',
#          dirname=dirname,
#          theme=theme,
#          automake_sphinx_options='',
#          split=False)

    # Dump all Unix commands run above as a Bash script
    bash = open('tmp_make.sh', 'w')
    print 'see tmp_make.sh for an equivalent auto-generated unix script'
    bash.write('''#!/bin/bash
set -x  # display all commands in output

# Safe execution of a Unix command: exit if failure
function system {
  "$@"
  if [ $? -ne 0 ]; then
    echo "make.sh: unsuccessful command $@"
    echo "abort!"
    exit 1
  fi
}
''')
    for cmd in unix_command_recorder:
        if cmd.startswith('doconce format') or cmd.startswith('rm '):
            bash.write('\n')  # delimiter line in script
        bash.write('system ' + cmd + '\n')
    bash.close()

    print 'see tmp_output.log for the output of all the commands'


if __name__ == '__main__':
    main()
