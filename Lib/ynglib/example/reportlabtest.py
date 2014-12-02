# -*- coding: utf-8 -*-

import ynglib
from ynglib.generators import reportlabPDF
from ynlib.colors import Color
from ynlib.system import Execute

c = ynglib.Canvas(210, 297, 'mm')

regular = '/Users/yanone/Downloads/adobe_source-sans-pro/SourceSansPro-Regular.ttf'


t = c.TextArea(font = regular, 
text = u'''Es geht um Widerstand gegen staatliche Kontrolle 

im Internet, wie schon der Name der Website verrät: resistsurveillance.org. Übersetzt bedeutet das: Widersetze Dich der Überwachung. Auf der Internetseite können Interessierte sich eine Software namens "Detekt" herunterladen, die Amnesty International und ein Bündnis aus Netzaktivisten veröffentlicht haben.''', 
fontsize = 20, x = 0, y = 0, charactersPerLine = 40, fillcolor=Color(CMYK=(1,1,1,100)))

t = c.TextArea(font = regular, 
text = u'''Es geht um Widerstand gegen staatliche Kontrolle im Internet, wie schon der Name der Website verrät: resistsurveillance.org. Übersetzt bedeutet das: Widersetze Dich der Überwachung. Auf der Internetseite können Interessierte sich eine Software namens "Detekt" herunterladen, die Amnesty International und ein Bündnis aus Netzaktivisten veröffentlicht haben.''', 
fontsize = 20, x = 0, y = 0 + c.pt2mm(t.calculatedHeight()), charactersPerLine = 40, height = 200, align='left', fillcolor=Color(CMYK=(1,1,1,100)))

c.NewPage()

c.Image('/Users/yanone/Inbox/Reham.jpg', 0, 0, width = 100, height = 100, position='35,50')

c.NewPage()



c.Generate(reportlabPDF.PDF("/Users/yanone/Code/git/Yanone/ynglib (trunk)/Lib/ynglib/example/test.pdf"))
Execute('open "/Users/yanone/Code/git/Yanone/ynglib (trunk)/Lib/ynglib/example/test.pdf"')

