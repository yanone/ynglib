import glib
from glib.generators import reportlabPDF

c = glib.Canvas(210, 297, 'mm')

c.Text(font = "/Users/yanone/Library/Fonts/dnk.ttf", text = 'hello', fontsize = 150, x = 100, y = 100, align='left', fillcolor=glib.CMYK(1,1,1,100))

c.Generate(reportlabPDF.PDF("/Users/yanone/Code/git/Yanone/glib.git (trunk)/Lib/glib/example/test.pdf"))
