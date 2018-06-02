import reportlab
#reload(reportlab)
import reportlab.pdfgen
import reportlab.pdfgen.canvas
##reload(reportlab.pdfgen)

from .base import BaseGeneratorDefinition
from reportlab.lib.units import mm
import os

class PDF(BaseGeneratorDefinition):
	def __init__(self, path):
		self.path = path
		self.registeredFonts = []
		self.Yfactor = 1.0
		
		# we know some glyphs are missing, suppress warnings
		import reportlab.rl_config
		reportlab.rl_config.warnOnMissingFontGlyphs = 0

	def Generate(self):
		self.unit = mm
		self.reportlabcanvas = reportlab.pdfgen.canvas.Canvas(self.path, pagesize=(self.Units(self.canvas.width), self.Units(self.canvas.height)))
		
		output = []
		
		# BG Color
		if self.canvas.bgcolor.hex != 'FFFFFF':
			self.setFillColor(self.canvas.bgcolor)
			self.reportlabcanvas.rect(0, 0, self.Units(self.canvas.width), self.Units(self.canvas.height), fill=1)
		
		# Walk objects
		for o in self.canvas.objects:
			output.extend(o.Generate(self))

		self.reportlabcanvas.showPage()
		self.reportlabcanvas.save()

	def Units(self, value):
		"""\
		Recalculate units to mm
		"""
		return value * self.unit

	def X(self, x):
		return x * self.unit

	def Y(self, y):
		return (self.canvas.height - y) * self.unit
#		return (y * self.Yfactor + self.canvas.height) * self.unit

	def setFillColor(self, color):
		if color.type == 'RGB':
			self.reportlabcanvas.setFillColorRGB(color.R/color.max, color.G/color.max, color.B/color.max)
		elif color.type == 'CMYK':
			self.reportlabcanvas.setFillColorCMYK(color.C/color.max, color.M/color.max, color.Y/color.max, color.K/color.max)

	def setStrokeColor(self, color):
		if color.type == 'RGB':
			self.reportlabcanvas.setStrokeColorRGB(color.R/color.max, color.G/color.max, color.B/color.max)
		elif color.type == 'CMYK':
			self.reportlabcanvas.setStrokeColorCMYK(color.C/color.max, color.M/color.max, color.Y/color.max, color.K/color.max)

#		self.reportlabcanvas.setStrokeColorRGB(color.R/color.max, color.G/color.max, color.B/color.max)

	def Line(self, o):
		self.reportlabcanvas.setLineWidth(o.strokewidth)
		self.setStrokeColor(o.strokecolor)
		self.reportlabcanvas.line(self.X(o.x1), self.Y(o.y1), self.X(o.x2), self.Y(o.y2))
		return ['']
		
	def Text(self, o):
		
		from reportlab.pdfbase import pdfmetrics
		from reportlab.pdfbase.ttfonts import TTFont
		if not os.path.basename(o.font) in self.registeredFonts:
			pdfmetrics.registerFont(TTFont(os.path.basename(o.font), o.font))
			self.registeredFonts.append(os.path.basename(o.font))

		if o.fillcolor:
			self.setFillColor(o.fillcolor)
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)

		self.reportlabcanvas.setFont(os.path.basename(o.font), o.fontsize)
		if o.align == 'left':
			self.reportlabcanvas.drawString(self.X(o.x), self.Y(o.y) - o.fontsize + .17*o.fontsize, o.text)
		elif o.align == 'center':
			self.reportlabcanvas.drawCentredString(self.X(o.x), self.Y(o.y) - o.fontsize + .17*o.fontsize, o.text)
		elif o.align == 'right':
			self.reportlabcanvas.drawRightString(self.X(o.x), self.Y(o.y) - o.fontsize + .17*o.fontsize, o.text)


		return ['']


	def TextArea(self, o):

		# Fonts
		from reportlab.pdfbase import pdfmetrics
		from reportlab.pdfbase.ttfonts import TTFont
		if not os.path.basename(o.font) in self.registeredFonts:
			pdfmetrics.registerFont(TTFont(os.path.basename(o.font), o.font))
			self.registeredFonts.append(os.path.basename(o.font))

		if o.fillcolor:
			self.setFillColor(o.fillcolor)
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)


		t = self.reportlabcanvas.beginText(self.X(o.x), self.Y(o.y) - o.fontsize + .17*o.fontsize)

		t.setFont(os.path.basename(o.font), o.fontsize)

		t.setTextRenderMode(0) # Fill

		for line in o.text.split('\n'):
			text = line
			t.textLine(text)
		
		self.reportlabcanvas.drawText(t)
		return ['']


	def Image(self, o):
		self.reportlabcanvas.drawInlineImage(o.path, self.X(o.x), self.Y(o.y) - o.height * self.unit, self.X(o.width), o.height * self.unit)
		return ['']

	def NewPage(self, o):
		self.reportlabcanvas.showPage()
		return ['']


	def Rect(self, o):
		if o.fillcolor:
			self.setFillColor(o.fillcolor)
			fill = 1
		else:
			fill = 0
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)
			stroke = 1
		else:
			stroke = 0
		if o.strokewidth:
			self.reportlabcanvas.setLineWidth(o.strokewidth)

		self.reportlabcanvas.rect(self.X(o.x), self.Y(o.y + o.height), self.X(o.width), o.height * self.unit, fill = fill, stroke = stroke)

		return ['']

	def Ellipse(self, o):
		if o.fillcolor:
			self.setFillColor(o.fillcolor)
			fill = 1
		else:
			fill = 0
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)
			stroke = 1
		else:
			stroke = 0
		if o.strokewidth:
			self.reportlabcanvas.setLineWidth(o.strokewidth)

		self.reportlabcanvas.ellipse(self.X(o.x), self.Y(o.y + o.height), self.X(o.x + o.width), self.Y(o.y), fill = fill, stroke = stroke)

		return ['']


	def BezierPathBegin(self, o):
		if o.fillcolor:
			self.setFillColor(o.fillcolor)
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)
		if o.strokewidth:
			self.reportlabcanvas.setLineWidth(o.strokewidth)
		self.bezierpath = self.reportlabcanvas.beginPath()
		return ['']

	def BezierPathEnd(self, o):
		self.reportlabcanvas.drawPath(self.bezierpath, stroke=0, fill=1)
		return ['']

	def BezierPathMoveTo(self, o):
		self.bezierpath.moveTo(self.X(o.x), self.Y(o.y))
		return ['']

	def BezierPathLineTo(self, o):
		self.bezierpath.lineTo(self.X(o.x), self.Y(o.y))
		return ['']

	def BezierPathCurveTo(self, o):
		self.bezierpath.curveTo(self.X(o.x1), self.Y(o.y1), self.X(o.x2), self.Y(o.y2), self.X(o.x3), self.Y(o.y3))
		return ['']

	def BezierPathClosePath(self, o):
		self.bezierpath.close()
		return ['']
