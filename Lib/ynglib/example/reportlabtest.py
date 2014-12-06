# -*- coding: utf-8 -*-

import ynglib
from ynglib.generators import reportlabPDF
from ynlib.colors import Color
from ynlib.system import Execute

c = ynglib.Canvas(210, 297, 'mm')

regular = '/Users/yanone/Downloads/adobe_source-sans-pro/SourceSansPro-Regular.ttf'

#c.Rect(0, 0, 210, 45, fillcolor = Color(hex='EDEDED'))
#c.Ellipse(0, 0, 210, 45, fillcolor = Color(hex='000000'))

#t = c.TextArea(font = regular, text = u'''Es geht um Widerstand gegen staatliche Kontrolle im Internet, wie schon der Name der Website verrät: resistsurveillance.org. Übersetzt bedeutet das: Widersetze Dich der Überwachung. Auf der Internetseite können Interessierte sich eine Software namens "Detekt" herunterladen, die Amnesty International und ein Bündnis aus Netzaktivisten veröffentlicht haben.''', fontsize = 20, x = 0, y = 0, charactersPerLine = 40, fillcolor=Color(CMYK=(1,1,1,100)))
#t = c.TextArea(font = regular, text = u'''Es geht um Widerstand gegen staatliche Kontrolle im Internet, wie schon der Name der Website verrät: resistsurveillance.org. Übersetzt bedeutet das: Widersetze Dich der Überwachung. Auf der Internetseite können Interessierte sich eine Software namens "Detekt" herunterladen, die Amnesty International und ein Bündnis aus Netzaktivisten veröffentlicht haben.''', fontsize = 20, x = 0, y = 0 + c.pt2mm(t.calculatedHeight()), charactersPerLine = 40, height = 200, align='left', fillcolor=Color(CMYK=(1,1,1,100)))

c.Text(font = regular, text='Hello', fontsize = 20, x = 0, y = 0)
c.TextArea(font = regular, text='Hello\nWorld', fontsize = 40, x = 50, y = 0, lineheight = 20)



c.Generate(reportlabPDF.PDF("/Users/yanone/Code/git/Yanone/ynglib (trunk)/Lib/ynglib/example/test.pdf"))
Execute('open "/Users/yanone/Code/git/Yanone/ynglib (trunk)/Lib/ynglib/example/test.pdf"')

