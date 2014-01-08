import ynglib
reload(ynglib)
from ynglib.fonts import CompositorFont
from ynglib.generators import NodeBox
from ynglib.generators import SaveAsSVG
reload(NodeBox)
reload(SaveAsSVG)
from ynlib.colors import Color

c = ynglib.Canvas(1000, 1000, 'px', bgcolor=Color(hex='E53456'))
c.TextPath(font = CompositorFont("/Users/yanone/Schriften/Font Produktion/2.0/Foundries/typemedia/Families/Heat/1.0/Fonts/OTF/Heat-Italic.otf"), text = 'hello', fontsize = 150, x = 500, y = 500, features=['calt', 'kern'], align='center', fillcolor=ynglib.RGBA(hex='000000'))
#c.Rect(50, 50, 200, 200, fillcolor=ynglib.RGBA(hex='00FFFF'), strokecolor=ynglib.RGBA(hex='00FF00'), strokewidth = 5.0)

c.Generate(NodeBox.NodeBox(canvas))
c.Generate(SaveAsSVG.SaveAsSVG("/Users/yanone/Code/Python/ynglib/example/test.svg"))
