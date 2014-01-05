from base import BaseGeneratorDefinition


class SaveAsSVG(BaseGeneratorDefinition):
	def __init__(self, path):
		self.path = path
	
	def Generate(self):
		
		output = []
		
		output.append('<?xml version="1.0" encoding="utf-8"?>')
		output.append('<!-- Generator: glib by Yanone -->')
		output.append('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">')
		output.append('<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="' + str(self.canvas.width) + str(self.canvas.units) + '" height="' + str(self.canvas.height) + str(self.canvas.units) + '">')

		# BG Color
		if self.canvas.bgcolor.A != 0:
			output.append('<rect x="-10" y="-10" width="%s" height="%s" fill="#%s" fill-opacity="%s" />' % (self.canvas.width + 20, self.canvas.height + 20, self.canvas.bgcolor.hex, self.canvas.bgcolor.A))
		
		# Walk objects
		for o in self.canvas.objects:
			output.extend(o.Generate(self))

		output.append('</svg>')
		
		from ynlib.files import WriteToFile
		from ynlib.system import Execute
		WriteToFile(self.path, ''.join(map(str, output)))
		# Compress
		if self.path.endswith('.svgz'):
#			print self.path
			Execute('gzip "%s"' % (self.path))
			Execute('mv "%s.gz" "%s"' % (self.path, self.path))
#			print 'gezipped'

	def Rect(self, o):
		output = '<rect x="%s" y="%s" width="%s" height="%s"' % (o.x, self.canvas.height - o.height - o.y, o.width, o.height)
		if o.fillcolor:
			output += ' fill="#%s"' % (o.fillcolor.hex)
		if o.fillcolor.A != 1.0:
			output += ' fill-opacity="%s"' % (o.fillcolor.A)
		if o.strokecolor:
			output += ' stroke="#%s"' % (o.strokecolor.hex)
			if o.strokecolor.A != 1.0:
				output += ' stroke-opacity="%s"' % (o.strokecolor.A)
		if o.strokewidth:
			output += ' stroke-width="%s"' % (o.strokewidth)
		output += ' />'
		return output

	def BezierPathBegin(self, o):
		output = []
		output.append('<g><path fill="#%s"' % (o.fillcolor.hex))
		if o.fillcolor.A != 1.0:
			output.append(' fill-opacity="%s"' % (o.fillcolor.A))
		if o.strokecolor:
			output.append(' stroke="#%s"' % (o.strokecolor.hex))
			if o.strokecolor.A != 1.0:
				output.append(' stroke-opacity="%s"' % (o.strokecolor.A))
		if o.strokewidth:
			output.append(' stroke-width="%s"' % (o.strokewidth))
		output.append(' d="')
		return output

	def BezierPathEnd(self, o):
		return ['"/></g>']

	def BezierPathMoveTo(self, o):
		return ["M %s %s" % (o.x, -o.y + self.canvas.height)]

	def BezierPathLineTo(self, o):
		return ["L %s %s" % (o.x, -o.y + self.canvas.height)]

	def BezierPathCurveTo(self, o):
		return ["C %s %s %s %s %s %s" % (o.x1, -o.y1 + self.canvas.height, o.x2, -o.y2 + self.canvas.height, o.x3, -o.y3 + self.canvas.height)]

	def BezierPathClosePath(self, o):
		return ["Z"]
