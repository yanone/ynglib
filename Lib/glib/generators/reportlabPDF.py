from base import BaseGeneratorDefinition
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

class PDF(BaseGeneratorDefinition):
	def __init__(self, path):
		self.path = path
		
		
		
		# we know some glyphs are missing, suppress warnings
		import reportlab.rl_config
		reportlab.rl_config.warnOnMissingFontGlyphs = 0

	def Generate(self):
		self.unit = mm
		self.reportlabcanvas = canvas.Canvas(self.path, pagesize=(self.Units(self.canvas.width), self.Units(self.canvas.height)))
		
		output = []
		
		# BG Color
		if self.canvas.bgcolor.A != 0:
			self.reportlabcanvas.setFillColorCMYK(self.canvas.bgcolor.C, self.canvas.bgcolor.M, self.canvas.bgcolor.Y, self.canvas.bgcolor.K)
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

	def setFillColor(self, color):
		self.reportlabcanvas.setFillColorCMYK(color.C / 100.0, color.M / 100.0, color.Y / 100.0, color.K / 100.0)

	def setStrokeColor(self, color):
		self.reportlabcanvas.setFillColorCMYK(color.C / 100.0, color.M / 100.0, color.Y / 100.0, color.K / 100.0)

	def Text(self, o):
		
		from reportlab.pdfbase.ttfonts import TTFont
		pdfmetrics.registerFont(TTFont('_font', o.font))
		canvas.setFont('_font', o.fontsize)

		if o.fillcolor:
			self.setFillColor(o.fillcolor)
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)

		self.reportlabcanvas.setFont(o.font, o.fontsize)
		if o.align == 'left':
			self.reportlabcanvas.drawString(self.Units(o.x), self.Units(o.y), o.text):
		elif o.align == 'center':
			self.reportlabcanvas.drawCentredString(self.Units(o.x), self.Units(o.y), o.text)
		elif o.align == 'right':
			self.reportlabcanvas.drawRightString(self.Units(o.x), self.Units(o.y), o.text)


		return ['']

	def Rect(self, o):
		if o.fillcolor:
			self.setFillColor(o.fillcolor)
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)
		if o.strokewidth:
			self.reportlabcanvas.setLineWidth(o.strokewidth)
		self.reportlabcanvas.rect(self.Units(o.x), self.Units(o.y), self.Units(o.width), self.Units(o.height), fill=1)
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
		self.bezierpath.moveTo(self.Units(o.x), self.Units(o.y))
		return ['']

	def BezierPathLineTo(self, o):
		self.bezierpath.lineTo(self.Units(o.x), self.Units(o.y))
		return ['']

	def BezierPathCurveTo(self, o):
		self.bezierpath.curveTo(self.Units(o.x1), self.Units(o.y1), self.Units(o.x2), self.Units(o.y2), self.Units(o.x3), self.Units(o.y3))
		return ['']

	def BezierPathClosePath(self, o):
		self.bezierpath.close()
		return ['']
