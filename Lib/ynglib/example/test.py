#!/usr/bin/env python

import ynglib, os
reload(ynglib)

from ynglib import Canvas
from ynglib.fonts import CompositorFont
from ynglib.generators import SaveAsSVG


c = Canvas(500, 500, 'px')
f = CompositorFont("/Users/yanone/Schriften/Font Produktion/Fonts/NonameSans-Regular.otf")
c.TextPath(f, text = 'abc', fontsize = 200, x = 50, y = 50, features=['calt', 'kern', 'smcp'], align = 'left')

print c.Generate(SaveAsSVG.SaveAsSVG())

