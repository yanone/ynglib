from base import BaseGeneratorDefinition
import fpdf, os

class PDF(BaseGeneratorDefinition):
	def __init__(self, path):
		self.path = path
		self.registeredFonts = []

	def SetFont(self, font, fontsize):
		
		fontName = os.path.splitext(os.path.basename(font))[0]

		# New
		if not fontName in self.registeredFonts:
			self.pdf.add_font(fontName, style='', fname=font, uni=True)
			self.registeredFonts.append(fontName)

		self.pdf.set_font(fontName,'',fontsize)

	
	def Generate(self):
		self.pdf = fpdf.FPDF('P' if self.canvas.height > self.canvas.width else 'L', self.canvas.units, (self.canvas.width, self.canvas.height))
		self.pdf.add_page()
		self.pdf.set_title(self.canvas.title)
		if self.canvas.author:
			self.pdf.set_author(self.canvas.author)
		
		# Walk objects
		for o in self.canvas.objects:
			#output.extend(o.Generate(self))
			o.Generate(self)

		self.pdf.close()
		
		# Save file
		self.pdf.output(self.path,'F')


	def SetFillColor(self, color):
		if color.type == 'RGB':
			self.pdf.set_fill_color(color.R, color.G, color.B)

	def SetStrokeColor(self, color):
		if color.type == 'RGB':
			self.pdf.set_draw_color(color.R, color.G, color.B)

	def SetTextColor(self, color):
		if color.type == 'RGB':
			self.pdf.set_text_color(color.R, color.G, color.B)


	def X(self, x):
		return x

	def Y(self, y):
		return y

	def Text(self, o):

		self.SetFont(o.font, o.fontsize)
		self.SetTextColor(o.fillcolor)
		self.pdf.text(o.x, o.y + self.canvas.pt2mm(o.fontsize - .17 * o.fontsize), o.text)

	def TextArea(self, o):

		self.SetFont(o.font, o.fontsize)
		self.SetTextColor(o.fillcolor)
		self.pdf.set_left_margin(o.x)
		self.pdf.set_xy(o.x, o.y)
		self.pdf.write(self.canvas.pt2mm(o.lineheight), txt = o.text)
		
	def Line(self, o):
		if o.strokecolor:
			self.SetStrokeColor(o.strokecolor)
		if o.strokewidth:
			self.pdf.set_line_width(self.canvas.pt2mm(o.strokewidth))

		self.pdf.line(o.x1, o.y1, o.x2, o.y2)


	def Rect(self, o):
		if o.fillcolor:
			self.SetFillColor(o.fillcolor)
			style = 'F'
		else:
			style = ''
		if o.strokecolor:
			self.SetStrokeColor(o.strokecolor)
			style += 'D'
		else:
			style += ''
		if o.strokewidth:
			self.pdf.set_line_width(self.canvas.pt2mm(o.strokewidth))

		self.pdf.rect(o.x, o.y, o.width, o.height, style = style)

	def Ellipse(self, o):
		if o.fillcolor:
			self.SetFillColor(o.fillcolor)
			style = 'F'
		else:
			style = ''
		if o.strokecolor:
			self.SetStrokeColor(o.strokecolor)
			style += 'D'
		else:
			style += ''
		if o.strokewidth:
			self.pdf.set_line_width(self.canvas.pt2mm(o.strokewidth))

		self.pdf.ellipse(o.x, o.y, o.width, o.height, style = style)

	def Image(self, o):
		self.pdf.image(o.path, o.x, o.y, o.width, o.height)
		return ['']

	def NewPage(self, o):
		self.pdf.add_page()
