from base import BaseGeneratorDefinition
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import reportlab, os

class PDF(BaseGeneratorDefinition):
	def __init__(self, path):
		self.path = path
		
		self.registeredFonts = []
		
		# we know some glyphs are missing, suppress warnings
		import reportlab.rl_config
		reportlab.rl_config.warnOnMissingFontGlyphs = 0

	def Generate(self):
		self.unit = mm
		self.reportlabcanvas = canvas.Canvas(self.path, pagesize=(self.Units(self.canvas.width), self.Units(self.canvas.height)))
		
		output = []
		
		# BG Color
		if self.canvas.bgcolor.A != 0:
			self.reportlabcanvas.setFillColorRGB(self.canvas.bgcolor.R, self.canvas.bgcolor.G, self.canvas.bgcolor.B)
			self.reportlabcanvas.rect(0, 0, self.canvas.width, self.canvas.height, fill=1)
		
		# Walk objects
		for o in self.canvas.objects:
			output.extend(o.Generate(self))

		self.reportlabcanvas.showPage()
		self.reportlabcanvas.save()

	def Units(self, value):
		u"""\
		Recalculate units to mm
		"""
		return value * self.unit

	def X(self, x):
		u"""\
		Recalculate units to mm
		"""
		return x * self.unit

	def Y(self, y):
		u"""\
		Recalculate units to mm
		"""
#		return (self.canvas.height + y * -1) * self.unit
		return (-y + self.canvas.height) * self.unit

	def setFillColor(self, color):
		self.reportlabcanvas.setFillColorRGB(color.R, color.G, color.B)

	def setStrokeColor(self, color):
		self.reportlabcanvas.setStrokeColorCMYK(color.R, color.G, color.B)

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
			self.reportlabcanvas.drawString(self.X(o.x), self.Y(o.y), o.text)
		elif o.align == 'center':
			self.reportlabcanvas.drawCentredString(self.X(o.x), self.Y(o.y), o.text)
		elif o.align == 'right':
			self.reportlabcanvas.drawRightString(self.X(o.x), self.Y(o.y), o.text)


		return ['']

	def Rect(self, o):
		if o.fillcolor:
			self.setFillColor(o.fillcolor)
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)
		if o.strokewidth:
			self.reportlabcanvas.setLineWidth(o.strokewidth)
		self.reportlabcanvas.rect(self.X(o.x), self.Y(o.y), self.X(o.width), self.X(o.height), fill=1)
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
