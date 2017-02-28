# -*- coding: UTF-8 -*-

########################################
# Color

from ynlib.colors import Color
import time, os, math
from ynlib.maths import Interpolate
from ynlib.system import Execute
from ynlib.strings import smartString

class Canvas(object):
	def __init__(self, width, height, units, bgcolor = Color(hex='FFFFFF'), strict = False, title = None, author = None):
		self.width = width
		self.height = height
		self.units = units
		self.bgcolor = bgcolor
		self.objects = []
		self.strict = strict
		self.title = title or "glib canvas created on %s" % (time.time())
		self.author = author

		self.mm = 2.834645669291339
	
	def Clear(self):
		u"""\
		Clear list of objects.
		"""
		self.objects = []
	
	def PageNumber(self):
		p = 1
		for o in self.objects:
			if o.__class__.__name__ == 'NewPage':
				p += 1
		return p

	def append(self, object):
		u"""\
		Append pre-initiated object to list
		"""
		self.objects.append(object)
		
	def TextPath(self, font, text, fontsize, x, y, features = [], align = 'left', fillcolor = Color(hex='000000'), strokecolor = None, strokewidth = 1.0):
		self.objects.append(TextPath(font, text, fontsize, x, y, features, align, fillcolor, strokecolor, strokewidth))
		
	def Text(self, font, text, fontsize, x, y, lineheight = None, features = [], featuresOff = [], language = None, align = 'left', fillcolor = Color(hex='000000'), strokecolor = None, strokewidth = 1.0):
		self.objects.append(Text(font, text, fontsize, x, y, lineheight, features, featuresOff, language, align, fillcolor, strokecolor, strokewidth))

	def TextArea(self, font, text, fontsize, x, y, width = None, height = None, charactersPerLine = None, lineheight = None, features = [], featuresOff = [], language = None, align = 'left', fillcolor = Color(hex='000000'), strokecolor = None, strokewidth = 1.0):
		t = TextArea(self, font, text, fontsize, x, y, width, height, charactersPerLine, lineheight, features, featuresOff, language, align, fillcolor, strokecolor, strokewidth)
		self.objects.append(t)
		return t

	def Image(self, path, x, y, width = None, height = None, unit = 'mm', position = '50,50', dpi = None):
		t = Image(path, x, y, width, height, unit, position, dpi)
		self.objects.append(t)
		return t

	def Rect(self, x, y, width, height, fillcolor = None, strokecolor = None, strokewidth = 1.0):
		self.objects.append( Rect(x, y, width, height, fillcolor, strokecolor, strokewidth) )

	def Ellipse(self, x, y, width, height, fillcolor = None, strokecolor = None, strokewidth = 1.0):
		self.objects.append( Ellipse(x, y, width, height, fillcolor, strokecolor, strokewidth) )
	
	def Generate(self, generator):
		
		self.generator = generator
		self.generator.canvas = self
		return self.generator.Generate()

	def Line(self, x1, y1, x2, y2, strokecolor = None, strokewidth = 1.0):
		self.objects.append( Line(x1, y1, x2, y2, strokecolor, strokewidth) )

	def Arrow(self, x1, y1, x2, y2, strokecolor = None, strokewidth = 1.0, beginning = False, end = True):
		self.objects.append( Arrow(x1, y1, x2, y2, strokecolor, strokewidth, beginning, end) )
		
	def NewPage(self):
		self.objects.append( NewPage() )

###


	def pt2mm(self, pt):
		u"""\
		Convert pt to mm.
		"""
		return pt * 0.352777778

	def mm2pt(self, mm):
		u"""\
		Convert mm to ts.
		"""
		return mm / 0.352777778

		

########################################
# graphic shapes


class NewPage(object):

	def Generate(self, generator):
		return generator.NewPage(self)


class Rect(object):
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

class Ellipse(object):
	def __init__(self, x, y, width, height, fillcolor, strokecolor, strokewidth):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.fillcolor = fillcolor
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth
	def Generate(self, generator):
		return generator.Ellipse(self)

class Line(object):
	def __init__(self, x1, y1, x2, y2, strokecolor, strokewidth):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth
	def Generate(self, generator):
		return generator.Line(self)

class Arrow(object):
	def __init__(self, x1, y1, x2, y2, strokecolor, strokewidth, beginning = False, end = True):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth
		self.beginning = beginning
		self.end = end

		arrowHeadLengthFactor = 2

		from ynlib.maths import Interpolate

		# Base Line
		self.baseline = BezierPath(None, self.strokecolor, self.strokewidth)
		self.baseline.MoveTo(self.x1, self.y1)
		self.baseline.LineTo(self.x2, self.y2)
		self.baseline.ClosePath()

		# Deltas
		if self.end:
			dx = self.x2 - self.x1
			dy = self.y2 - self.y1

			# Senkrechte links und rechts
			psl = (self.x2 - dy, self.y2 + dx)
			psr = (self.x2 + dy, self.y2 - dx)

			# Aussenpunkte
			pal = (Interpolate(self.x1, psl[0], .5), Interpolate(self.y1, psl[1], .5))
			par = (Interpolate(self.x1, psr[0], .5), Interpolate(self.y1, psr[1], .5))

			# Länge
			normallaenge = math.sqrt((self.x2 - pal[0])**2 + (self.y2 - pal[1])**2)
			laenge = self.strokewidth * arrowHeadLengthFactor

			# finalepunkte
			pfl = (self.x2 - (self.x2 - pal[0]) / normallaenge * laenge, self.y2 - (self.y2 - pal[1]) / normallaenge * laenge)
			pfr = (self.x2 - (self.x2 - par[0]) / normallaenge * laenge, self.y2 - (self.y2 - par[1]) / normallaenge * laenge)

			self.endarrowhead = BezierPath(None, self.strokecolor, self.strokewidth)
			self.endarrowhead.MoveTo(pfl[0], pfl[1])
			self.endarrowhead.LineTo(self.x2, self.y2)
			self.endarrowhead.LineTo(pfr[0], pfr[1])

		if self.beginning:

			dx = self.x1 - self.x2
			dy = self.y1 - self.y2

			# Senkrechte links und rechts
			psl = (self.x1 - dy, self.y1 + dx)
			psr = (self.x1 + dy, self.y1 - dx)

			# Aussenpunkte
			pal = (Interpolate(self.x2, psl[0], .5), Interpolate(self.y2, psl[1], .5))
			par = (Interpolate(self.x2, psr[0], .5), Interpolate(self.y2, psr[1], .5))

			# Länge
			normallaenge = math.sqrt((self.x1 - pal[0])**2 + (self.y1 - pal[1])**2)
			laenge = self.strokewidth * arrowHeadLengthFactor

			# finalepunkte
			pfl = (self.x1 - (self.x1 - pal[0]) / normallaenge * laenge, self.y1 - (self.y1 - pal[1]) / normallaenge * laenge)
			pfr = (self.x1 - (self.x1 - par[0]) / normallaenge * laenge, self.y1 - (self.y1 - par[1]) / normallaenge * laenge)

			self.beginningarrowhead = BezierPath(None, self.strokecolor, self.strokewidth)
			self.beginningarrowhead.MoveTo(pfl[0], pfl[1])
			self.beginningarrowhead.LineTo(self.x1, self.y1)
			self.beginningarrowhead.LineTo(pfr[0], pfr[1])


	def Generate(self, generator):

		_list = []
		_list.extend(self.baseline.Generate(generator))
		if self.beginning:
			_list.extend(self.beginningarrowhead.Generate(generator))
		if self.end:
			_list.extend(self.endarrowhead.Generate(generator))
		return _list

class Text(object):
	def __init__(self, font, text, fontsize, x, y, lineheight, features, featuresOff, language, align, fillcolor, strokecolor, strokewidth):
		self.font = font
		self.text = smartString(text)
		self.fontsize = fontsize
		self.lineheight = lineheight or self.fontsize * 1.2
		self.x = x
		self.y = y
		self.features = features
		self.featuresOff = featuresOff
		self.language = language
		self.fillcolor = fillcolor
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth
		self.align = align

	def Generate(self, generator):
		return generator.Text(self)

	def __repr__(self):
		return '<Text "%s">' % self.text[:80]


class TextArea(object):
	def __init__(self, parent, font, text, fontsize, x, y, width, height, charactersPerLine, lineheight, features, featuresOff, language, align, fillcolor, strokecolor, strokewidth):

		from ynlib.strings import SimpleTextWrap

		self.parent = parent
		self.font = font
		self.fontsize = fontsize
		self.lineheight = lineheight or self.fontsize * 1.2
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.charactersPerLine = charactersPerLine
		
		if self.charactersPerLine:
			self.text = SimpleTextWrap(smartString(text), self.charactersPerLine)
		else:
			self.text = smartString(text)

		self.features = features
		self.featuresOff = featuresOff
		self.language = language
		self.fillcolor = fillcolor
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth
		self.align = align

	def calculatedHeight(self):
		return len(self.text.split('\n')) * self.lineheight

	def Generate(self, generator):
		return generator.TextArea(self)

	def __repr__(self):
		return '<TextArea "%s">' % self.text[:80].replace('\n', '\\n')


class Image(object):
	def __init__(self, path, x, y, width, height, unit, position, dpi):
		
		self.path = path
		self.croppedPath = None
		self.croppedCommand = None
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.unit = unit
		self.dpi = dpi
		self.position = [x / 100.0 for x in map(int, position.split(','))]

		# Pull info from file
		from ynlib.imaging import imageFileDimensions
		self.fileDimensions = imageFileDimensions(self.path)
		self.fileAspectRatio = float(self.fileDimensions[0]) / float(self.fileDimensions[1])

		# width or height is missing, so calc the other using image pixel dimensions.
		if bool(self.width) != bool(self.height):
		
			if self.width and not self.height:
				self.height = self.getHeight(self.width)
			elif self.height and not self.width:
				self.width = self.getWidth(self.height)
		

		# both width and height are given, so fit image into the frame using cropping and the middle point ("position")
		else:
			targetAspectRatio = float(self.width) / float(self.height)
			
			# target wider than file
			if targetAspectRatio > self.fileAspectRatio:
				fileResolution = self.fileDimensions[0] / float(self.width)
			
			# target taller than file
			else:
				fileResolution = self.fileDimensions[1] / float(self.height)
			
			targetPixelDimensions = [x * fileResolution for x in [self.width, self.height]]
		
			self.croppedPath = os.path.join(os.path.dirname(self.path), 'temp.jpg')
			self.croppedCommand = 'convert "%s" -crop %sx%s+%s+%s\! "%s"' % (self.path, int(targetPixelDimensions[0]), int(targetPixelDimensions[1]), int((self.fileDimensions[0] - targetPixelDimensions[0]) * self.position[0]), int((self.fileDimensions[1] - targetPixelDimensions[1]) * self.position[1]), self.croppedPath)
			print self.croppedCommand
		

	def getWidth(self, height):
		return height * self.fileAspectRatio

	def getHeight(self, width):
		return width / self.fileAspectRatio

	def Generate(self, generator):
		
		if self.croppedPath:
			Execute(self.croppedCommand)
			self.path = self.croppedPath
		
		i = generator.Image(self)
		
		os.remove(self.croppedPath)
		
		return i

	
class TextPath(object):
	def __init__(self, font, text, fontsize, x, y, features, align, fillcolor, strokecolor, strokewidth):
		self.font = font
		self.text = smartString(text)
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

class BezierPath(object):
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

class BezierPathMoveTo(object):
	def __init__(self, bezierpath, x, y):
		self.bezierpath = bezierpath
		self.x = x
		self.y = y
	def Generate(self, generator):
		return generator.BezierPathMoveTo(self)

class BezierPathLineTo(object):
	def __init__(self, bezierpath, x, y):
		self.bezierpath = bezierpath
		self.x = x
		self.y = y
	def Generate(self, generator):
		return generator.BezierPathLineTo(self)

class BezierPathCurveTo(object):
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

class BezierPathClosePath(object):
	def __init__(self, bezierpath):
		self.bezierpath = bezierpath
	def Generate(self, generator):
		return generator.BezierPathClosePath(self)

