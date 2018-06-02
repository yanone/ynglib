from .base import BaseGeneratorDefinition

from .nodebox import graphics
from .nodebox import util
from . import nodebox

class NodeBox(BaseGeneratorDefinition):
	def __init__(self, nodeboxcanvas):
		self.nodeboxcanvas = nodeboxcanvas

	def Generate(self):
		self.namespace = {}
		self.context = graphics.Context(self.nodeboxcanvas, self.namespace)
		output = []
		output.append('size(%s, %s)' % (self.canvas.width, self.canvas.height))
		# BG Color
		output.append('background(%s, %s, %s, %s)' % (self.canvas.bgcolor.R, self.canvas.bgcolor.G, self.canvas.bgcolor.B, self.canvas.bgcolor.A))

		# Walk objects
		for o in self.canvas.objects:
			output.extend(o.Generate(self))

		string = '\n'.join(map(str, output))
		self.run(string)

	def Rect(self, o):
		output = []
		if o.fillcolor:
			output.append('fill(%s, %s, %s, %s)' % (o.fillcolor.R, o.fillcolor.G, o.fillcolor.B, o.fillcolor.A))
		else:
			output.append('nofill()')
		if o.strokecolor:
			output.append('stroke(%s, %s, %s, %s)' % (o.strokecolor.R, o.strokecolor.G, o.strokecolor.B, o.strokecolor.A))
		else:
			output.append('nostroke()')
		if o.strokewidth:
			output.append('strokewidth(%s)' % (o.strokewidth))
		output.append('rect(%s, %s, %s, %s)' % (o.x, -o.y + self.canvas.height, o.width, -o.height))
		return output

	def BezierPathBegin(self, o):
		output = []
		output.append('path = BezierPath()')
		if o.fillcolor:
			output.append('fill(%s, %s, %s, %s)' % (o.fillcolor.R, o.fillcolor.G, o.fillcolor.B, o.fillcolor.A))
		else:
			output.append('nofill()')
		if o.strokecolor:
			output.append('stroke(%s, %s, %s, %s)' % (o.strokecolor.R, o.strokecolor.G, o.strokecolor.B, o.strokecolor.A))
		else:
			output.append('nostroke()')
		if o.strokewidth:
			output.append('strokewidth(%s)' % (o.strokewidth))
		return output

	def BezierPathEnd(self, o):
		return ['drawpath(path)']

	def BezierPathMoveTo(self, o):
		return ['path.moveto(%s, %s)' % (o.x, -o.y + self.canvas.height)]
		
	def BezierPathLineTo(self, o):
		return ['path.lineto(%s, %s)' % (o.x, -o.y + self.canvas.height)]

	def BezierPathCurveTo(self, o):
		return ['path.curveto(%s, %s, %s, %s, %s, %s)' % (o.x1, -o.y1 + self.canvas.height, o.x2, -o.y2 + self.canvas.height, o.x3, -o.y3 + self.canvas.height)]

	def BezierPathClosePath(self, o):
		return ['path.closepath()']

	def _initNamespace(self, frame=1):
		self.nodeboxcanvas.clear()
		self.namespace.clear()
		# Add everything from the namespace
		for name in graphics.__all__:
			self.namespace[name] = getattr(graphics, name)
		for name in util.__all__:
			self.namespace[name] = getattr(util, name)
		# Add everything from the context object
		self.namespace["_ctx"] = self.context
		for attrName in dir(self.context):
			self.namespace[attrName] = getattr(self.context, attrName)
		# Add the document global
		self.namespace["__doc__"] = self.__doc__
		# Add the frame
#		self.frame = frame
#		self.namespace["PAGENUM"] = self.namespace["FRAME"] = self.frame
#		self.namespace["path"] = self.namespace["path"] = self.NBbezierpath

	def run(self, source_or_code):
		self._initNamespace()
		if isinstance(source_or_code, str):
			source_or_code = compile(source_or_code + "\n\n", "<Untitled>", "exec")
		exec(source_or_code, self.namespace)
