########################################
# Color

import ynlib.colors
import time
from ynlib.maths import Interpolate

class RGBA:
	def __init__(self, hex = None, R = None, G = None, B = None, A = 1.0):
		if hex:
			self.R, self.G, self.B = ynlib.colors.HextoRGB(hex)
			self.hex = hex
		else:
			self.R = R
			self.G = G
			self.B = B
			self.updateHex()
		self.A = A
	
	def updateHex(self):
			self.hex = ynlib.colors.RGBtoHex((self.R, self.G, self.B)).upper()

	def __add__(self, other):
		u"""\
		Darken by float 0...1
		"""
		if isinstance(other, float):
			return RGBA(R=Interpolate(self.R, 1, other), G=Interpolate(self.G, 1, other), B=Interpolate(self.B, 1, other))

	def __sub__(self, other):
		u"""\
		Lighten by float 0...1
		"""
		if isinstance(other, float):
			return RGBA(R=Interpolate(self.R, 0, other), G=Interpolate(self.G, 0, other), B=Interpolate(self.B, 0, other))
	
	def __repr__(self):
		return "<RGBA %s %s %s>" % (self.R, self.G, self.B)

class CMYK:
	def __init__(self, C, M, Y, K, A = 1.0):
		u"""\
		CMYK values from 0 to 100
		"""
		self.C = C
		self.M = M
		self.Y = Y
		self.K = K
		self.A = A

	def __repr__(self):
		return "<CMYK %s %s %s %s>" % (self.C, self.M, self.Y, self.K)

	def __sub__(self, other):
		u"""\
		Darken by float 0...1
		"""
		if isinstance(other, float):
			return CMYK(Interpolate(self.C, 100, other), Interpolate(self.M, 100, other), Interpolate(self.Y, 100, other), Interpolate(self.K, 100, other))

	def __add__(self, other):
		u"""\
		Lighten by float 0...1
		"""
		if isinstance(other, float):
			return CMYK(Interpolate(self.C, 0, other), Interpolate(self.M, 0, other), Interpolate(self.Y, 0, other), Interpolate(self.K, 0, other))


class Canvas:
	def __init__(self, width, height, units, bgcolor = RGBA(R=0, G=0, B=0, A=0), strict = False, title = None):
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
		
	def TextPath(self, font, text, fontsize, x, y, features = [], align = 'left', fillcolor = RGBA(R=0, G=0, B=0), strokecolor = None, strokewidth = 1.0):
		self.objects.append(TextPath(font, text, fontsize, x, y, features, align, fillcolor, strokecolor, strokewidth))

	def Rect(self, x, y, width, height, fillcolor = None, strokecolor = None, strokewidth = 1.0):
		self.objects.append( Rect(self, x, y, width, height, fillcolor, strokecolor, strokewidth) )
	
	def Generate(self, generator):
		
		self.generator = generator
		self.generator.canvas = self
		self.generator.Generate()



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

	
class TextPath:
	def __init__(self, font, text, fontsize, x, y, features = [], align = 'left', fillcolor = RGBA(R=0, G=0, B=0), strokecolor = None, strokewidth = 1.0):
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

