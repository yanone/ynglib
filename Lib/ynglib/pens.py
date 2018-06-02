from fontTools.pens.basePen import BasePen

class BezierPathPen(BasePen):
	"""\
	...
	"""

	def __init__(self, bezierpath, glyphSet, x, y, scale):
		BasePen.__init__(self, glyphSet)
		self.bezierpath = bezierpath
		self.x = x
		self.y = y
		self.scale = float(scale)

	def _moveTo(self, xxx_todo_changeme):
		(x,y) = xxx_todo_changeme
		x = x + self.x
		y = y + self.y	
		self.bezierpath.MoveTo(x * self.scale, y * self.scale)

	def _lineTo(self, xxx_todo_changeme1):
		(x,y) = xxx_todo_changeme1
		x = x + self.x
		y = y + self.y	
		self.bezierpath.LineTo(x * self.scale, y * self.scale)

	def _curveToOne(self, xxx_todo_changeme2, xxx_todo_changeme3, xxx_todo_changeme4):
		(x1,y1) = xxx_todo_changeme2
		(x2,y2) = xxx_todo_changeme3
		(x3,y3) = xxx_todo_changeme4
		x1 = x1 + self.x	
		x2 = x2 + self.x	
		x3 = x3 + self.x	
		y1 = y1 + self.y	
		y2 = y2 + self.y	
		y3 = y3 + self.y	
		self.bezierpath.CurveTo(x1 * self.scale, y1 * self.scale, x2 * self.scale, y2 * self.scale, x3 * self.scale, y3 * self.scale)

	def _closePath(self):
		self.bezierpath.ClosePath()

	def _endPath(self):
		pass

