#!/usr/bin/env python

import ynglib
reload(ynglib)

from ynglib import Canvas
from ynglib.fonts import CompositorFont
from ynglib.generators import wxWindow, VanillaWindow


c = Canvas(500, 500, 'px')
f = font = CompositorFont("/Users/yanone/Schriften/Font Produktion/2.0/Foundries/typemedia/Families/Heat/1.0/Fonts/OTF/Heat-Italic.otf")
c.TextPath(f, text = 'abc', fontsize = 200, x = 250, y = 250, features=['calt', 'kern'], align = 'left')
c.Generate(VanillaWindow.VanillaWindow())

