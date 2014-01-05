import glib#
reload(glib)
#from glib.fonts import CompositorFont
from glib.generators import reportlabPDF
#reload(reportlabPDF)

c = glib.Canvas(210, 297, 'mm')

#c.TextPath(font = CompositorFont("/Users/yanone/Schriften/Font Produktion/2.0/Foundries/typemedia/Families/Heat/1.0/Fonts/OTF/Heat-Italic.otf"), text = 'hello', fontsize = 150, x = 500, y = 500, features=['calt', 'kern'], align='center', fillcolor=glib.RGBA(hex='000000'))
#c.Rect(50, 50, 200, 200, fillcolor=glib.RGBA(hex='00FFFF'), strokecolor=glib.RGBA(hex='00FF00'), strokewidth = 5.0)

c.Text(font = "/Users/yanone/Inbox/NittiPXLight.ttf", text = 'hello', fontsize = 150, x = 100, y = 100, align='left', fillcolor=glib.CMYK(0,0,0,0))

c.Generate(reportlabPDF.PDF("/Users/yanone/Code/git/Yanone/glib.git (trunk)/Lib/glib/example/test.pdf"))
