########################################
# Color

from ynlib.colors import Color
import time
from ynlib.maths import Interpolate

class Canvas:
	def __init__(self, width, height, units, bgcolor = Color(hex='FFFFFF'), strict = False, title = None):
		self.width = width
		self.height = height
		self.units = units
		self.bgcolor = bgcolor
		self.objects = []
		self.strict = strict
		self.title = title
		if not self.title:
			self.title = "glib canvas created on %s" % (time.time())
	
	def Clear(self):
		u"""\
		Clear list of objects.
		"""
		self.objects = []
	
	def append(self, object):
		u"""\
		Append pre-initiated object to list
		"""
		self.objects.append(object)
		
	def TextPath(self, font, text, fontsize, x, y, features = [], align = 'left', fillcolor = Color(hex='000000'), strokecolor = None, strokewidth = 1.0):
		self.objects.append(TextPath(font, text, fontsize, x, y, features, align, fillcolor, strokecolor, strokewidth))
		
	def Text(self, font, text, fontsize, x, y, lineheight = None, features = [], align = 'left', fillcolor = Color(hex='000000'), strokecolor = None, strokewidth = 1.0):
		self.objects.append(Text(font, text, fontsize, x, y, lineheight, features, align, fillcolor, strokecolor, strokewidth))

	def Rect(self, x, y, width, height, fillcolor = None, strokecolor = None, strokewidth = 1.0):
		self.objects.append( Rect(self, x, y, width, height, fillcolor, strokecolor, strokewidth) )
	
	def Generate(self, generator):
		
		self.generator = generator
		self.generator.canvas = self
		self.generator.Generate()

	def Line(self, x1, y1, x2, y2, strokecolor = None, strokewidth = 1.0):
		self.objects.append( Line(x1, y1, x2, y2, strokecolor, strokewidth) )
		

########################################
# graphic shapes


class Rect:
	def __init__(self, x, y, width, height, fillcolor, strokecolor, strokewidth):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.fillcolor = fillcolor
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth
	def Generate(self, generator):
		return generator.Rect(self)

class Line:
	def __init__(self, x1, y1, x2, y2, strokecolor, strokewidth):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth
	def Generate(self, generator):
		return generator.Line(self)

class Text:
	def __init__(self, font, text, fontsize, x, y, lineheight = None, features = [], align = 'left', fillcolor = Color(hex='000000'), strokecolor = None, strokewidth = 1.0):
		self.font = font
		self.text = text
		self.fontsize = fontsize
		self.lineheight = lineheight
		self.x = x
		self.y = y
		self.features = features
		self.fillcolor = fillcolor
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth
		self.align = align

	def Generate(self, generator):
		return generator.Text(self)
	
class TextPath:
	def __init__(self, font, text, fontsize, x, y, features = [], align = 'left', fillcolor = Color(hex='000000'), strokecolor = None, strokewidth = 1.0):
		self.font = font
		self.text = text
		self.fontsize = fontsize
		self.x = x
		self.y = y
		self.features = features
		self.fillcolor = fillcolor
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth

		self.bezierpath = BezierPath(self.fillcolor, self.strokecolor, self.strokewidth)
		self.scale = float(self.fontsize) / float(font.comp.source['head'].unitsPerEm)
		self.glyphrecords = self.GlyphRecords(font, text, features)
		self.textwidth = self.TextWidth()
		self.width = self.textwidth*self.scale
		
		# justification
		if align == 'left':
			_x = 0
		elif align == 'center':
			_x = -self.textwidth*self.scale / 2.0
		elif align == 'right':
			_x = -self.textwidth*self.scale
			
		# process glyphs
		from pens import BezierPathPen
		for glyphset, glyphrecord in self.glyphrecords:
			pen = BezierPathPen(self.bezierpath, glyphset, (self.x + _x) / self.scale, self.y / self.scale, self.scale)
			glyphset.draw(pen)
			_x += (glyphset.width + glyphrecord.xAdvance + glyphrecord.xPlacement) * self.scale

	def Generate(self, generator):
		return self.bezierpath.Generate(generator)

	def TextWidth(self):
		w = 0
		for glyphset, glyphrecord in self.glyphrecords:
			w += (glyphset.width + glyphrecord.xAdvance + glyphrecord.xPlacement)
		return w

	def GlyphRecords(self, font, text, features):
		u"""\
		Process a string on a font file using compositor. Returns (glyphsets, glyphrecords).
		"""

		returnlist = []

		# Apply features
		for feature in features:
			font.comp.setFeatureState(feature, True)

		# Process
		glyphrecords = font.comp.process(text)
		for glyphrecord in glyphrecords:
			returnlist.append((font.comp.glyphSet[glyphrecord.glyphName], glyphrecord))

		return returnlist




########################################
# Bezier

class BezierPath:
	def __init__(self, fillcolor, strokecolor, strokewidth):
		self.commands = []
		self.fillcolor = fillcolor
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth
	
	def MoveTo(self, x, y):
		self.commands.append( BezierPathMoveTo(self, x, y) )
	
	def LineTo(self, x, y):
		self.commands.append( BezierPathLineTo(self, x, y) )

	def CurveTo(self, x1, y1, x2, y2, x3, y3):
		self.commands.append( BezierPathCurveTo(self, x1, y1, x2, y2, x3, y3) )
	
	def ClosePath(self):
		self.commands.append( BezierPathClosePath(self) )

	def Generate(self, generator):
		returns = []
		returns.extend( generator.BezierPathBegin(self) )
		for command in self.commands:
			returns.extend( command.Generate(generator) )
		returns.extend(generator.BezierPathEnd(self))
		return returns

class BezierPathMoveTo:
	def __init__(self, bezierpath, x, y):
		self.bezierpath = bezierpath
		self.x = x
		self.y = y
	def Generate(self, generator):
		return generator.BezierPathMoveTo(self)

class BezierPathLineTo:
	def __init__(self, bezierpath, x, y):
		self.bezierpath = bezierpath
		self.x = x
		self.y = y
	def Generate(self, generator):
		return generator.BezierPathLineTo(self)

class BezierPathCurveTo:
	def __init__(self, bezierpath, x1, y1, x2, y2, x3, y3):
		self.bezierpath = bezierpath
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.x3 = x3
		self.y3 = y3
	def Generate(self, generator):
		return generator.BezierPathCurveTo(self)

class BezierPathClosePath:
	def __init__(self, bezierpath):
		self.bezierpath = bezierpath
	def Generate(self, generator):
		return generator.BezierPathClosePath(self)

