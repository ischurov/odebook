## -*- coding: utf-8 -*-

<%
import sys
sys.path.insert(0, '.')
# Allow imports from local dir to import nesode and odebook

import matplotlib
matplotlib.use('Agg')
# Need this to plot pictures without graphical backend

import nesode as no
from odebook import needfigure, savefigs,mkfig
import odebook as book 
%>

<%def name="begin_question()">
## sphinx doesn't allow quizes inside questions
% if FORMAT == 'sphinx':
__Контрольный вопрос.__ 
% else:
!bquestion Контрольный вопрос
%endif
</%def>

<%def name="end_question()">
% if FORMAT != 'sphinx':
!equestion
%endif
</%def>

<%
def snippet(title, id):
    if FORMAT == 'html':
        return u"<a class='snippet-ref' data-url='snippets/{id}.html'>{title}</a>".format(id=id, title=title)
    else:
        return title
%>
<%
no.rcParams['figure.figsize']=(8,6)
%>
<%def name="details(*refs)">
% if FORMAT == 'html':
Подробнее: ${", ".join("ref{%s}" % ref for ref in refs)}.
% else:
Подробнее см. в 
% if len(refs) == 1:
параграфе ref{${refs[0]}}.
% else:
параграфах ${", ".join("ref{%s}" % ref for ref in refs)}.
% endif
% endif
</%def>

