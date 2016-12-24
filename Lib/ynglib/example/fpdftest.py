# -*- coding: utf-8 -*-

import ynglib
from ynglib.generators import pyfpdf
reload(pyfpdf)
from ynlib.colors import Color
from ynlib.system import Execute

c = ynglib.Canvas(210, 297, 'mm', title = 'ABC', author = 'Yanone')

regular = '/Users/yanone/Projekte/Bold Monday/03 - Nitti Vietnamese/4.0/Back to Bold Monday/Nitti Extended Latin 01/TTF/Nitti PX Normal.ttf'

c.Rect(0, 0, 210, 45, fillcolor = Color(hex='EDEDED'))
c.Rect(0, 0, 210, 45, strokecolor = Color(hex='0D0D0D'), strokewidth = 2)
c.Ellipse(0, 0, 210, 45, fillcolor = Color(hex='00F00F'), strokecolor = Color(hex='F0F00F'))

#t = c.TextArea(font = regular, text = u'''Es geht um Widerstand gegen staatliche Kontrolle im Internet, wie schon der Name der Website verrät: resistsurveillance.org. Übersetzt bedeutet das: Widersetze Dich der Überwachung. Auf der Internetseite können Interessierte sich eine Software namens "Detekt" herunterladen, die Amnesty International und ein Bündnis aus Netzaktivisten veröffentlicht haben.''', fontsize = 20, x = 0, y = 0, charactersPerLine = 40, fillcolor=Color(CMYK=(1,1,1,100)))
#t = c.TextArea(font = regular, text = u'''Es geht um Widerstand gegen staatliche Kontrolle im Internet, wie schon der Name der Website verrät: resistsurveillance.org. Übersetzt bedeutet das: Widersetze Dich der Überwachung. Auf der Internetseite können Interessierte sich eine Software namens "Detekt" herunterladen, die Amnesty International und ein Bündnis aus Netzaktivisten veröffentlicht haben.''', fontsize = 20, x = 0, y = 0 + c.pt2mm(t.calculatedHeight()), charactersPerLine = 40, height = 200, align='left', fillcolor=Color(CMYK=(1,1,1,100)))

c.Text(font = regular, text='Hello', fontsize = 20, x = 0, y = 0)
c.Text(font = regular, text='Hello', fontsize = 40, x = 0, y = 0)
c.TextArea(font = regular, text='Hello\nWorld', fontsize = 40, x = 0, y = 0, lineheight = 40)

c.NewPage()

c.Image('/Users/yanone/Inbox/Reham.jpg', 10, 10, 50, 30)

c.Generate(pyfpdf.PDF("/Users/yanone/Code/git/Yanone/ynglib (trunk)/Lib/ynglib/example/test.pdf"))
Execute('open "/Users/yanone/Code/git/Yanone/ynglib (trunk)/Lib/ynglib/example/test.pdf"')

