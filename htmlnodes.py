# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from docutils.nodes import Element, General, Inline, Part, Referential, \
                           TextElement


class figcaption(Part, TextElement):
    pass


class div(Part, Element):
    pass


class img(General, Inline, Element):
    pass


class a(General, Inline, Referential, TextElement):
    pass
