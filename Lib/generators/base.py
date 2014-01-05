########################################
# generator definitions

class BaseGeneratorDefinition:
	def __init__(self):
		self.canvas = None

	def Rect(self, o = None):
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

	def Generate(self):
		pass

