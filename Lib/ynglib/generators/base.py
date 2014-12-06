########################################
# generator definitions

# origin: bottom left
class BaseGeneratorDefinition:
	def __init__(self):
		self.canvas = None
		self.Yfactor = 1.0

	def Rect(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def Ellipse(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def Line(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def BezierPathBegin(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def BezierPathEnd(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def BezierPathMoveTo(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def BezierPathLineTo(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def BezierPathCurveTo(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def BezierPathClosePath(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def Text(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def TextArea(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def Image(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def NewPage(self, o = None):
		if self.canvas.strict: raise NotImplementedError

	def Generate(self):
		pass

