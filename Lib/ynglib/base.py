########################################
# Color

from ynlib.colors import Color
import time, os
from ynlib.maths import Interpolate
from ynlib.system import Execute

class Canvas(object):
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

	def TextArea(self, font, text, fontsize, x, y, width = None, height = None, charactersPerLine = None, lineheight = None, features = [], align = 'left', fillcolor = Color(hex='000000'), strokecolor = None, strokewidth = 1.0):
		t = TextArea(self, font, text, fontsize, x, y, width, height, charactersPerLine, lineheight, features, align, fillcolor, strokecolor, strokewidth)
		self.objects.append(t)
		return t

	def Image(self, path, x, y, width = None, height = None, unit = 'mm', position = '50,50', dpi = None):
		t = Image(path, x, y, width, height, unit, position, dpi)
		self.objects.append(t)
		return t

	def Rect(self, x, y, width, height, fillcolor = None, strokecolor = None, strokewidth = 1.0):
		self.objects.append( Rect(self, x, y, width, height, fillcolor, strokecolor, strokewidth) )
	
	def Generate(self, generator):
		
		self.generator = generator
		self.generator.canvas = self
		self.generator.Generate()

	def Line(self, x1, y1, x2, y2, strokecolor = None, strokewidth = 1.0):
		self.objects.append( Line(x1, y1, x2, y2, strokecolor, strokewidth) )
		
	def NewPage(self):
		self.objects.append( NewPage() )

###


	def pt2mm(self, pt):
		u"""\
		Convert pt to mm.
		"""
		return pt * 0.352777778

		

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

class Text(object):
	def __init__(self, font, text, fontsize, x, y, lineheight, features, align, fillcolor, strokecolor, strokewidth):
		self.font = font
		self.text = text
		self.fontsize = fontsize
		self.lineheight = lineheight or self.fontsize * 1.2
		self.x = x
		self.y = y
		self.features = features
		self.fillcolor = fillcolor
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth
		self.align = align

	def Generate(self, generator):
		return generator.Text(self)

class TextArea(object):
	def __init__(self, parent, font, text, fontsize, x, y, width, height, charactersPerLine, lineheight, features, align, fillcolor, strokecolor, strokewidth):

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
		self.text = SimpleTextWrap(text, self.charactersPerLine)
		self.features = features
		self.fillcolor = fillcolor
		self.strokecolor = strokecolor
		self.strokewidth = strokewidth
		self.align = align

	def calculatedHeight(self):
		return len(self.text.split('\n')) * self.lineheight

	def Generate(self, generator):
		return generator.TextArea(self)


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

