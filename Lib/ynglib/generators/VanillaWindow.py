from .base import BaseGeneratorDefinition

import vanilla
from vanilla.test.testTools import executeVanillaTest

import objc
from AppKit import *

class DrawingWindow(object):

	def __init__(self, size):
		self.w = vanilla.Window(size)
		self.w.image = vanilla.ImageView((0, 0, size[0], size[1]))

class VanillaWindow(BaseGeneratorDefinition):
	def __init__(self):
		self.window = None
		self.windowOpen = False

	def Generate(self):
		output = []

#		executeVanillaTest(DrawingWindow)

		# Initialize vanilla window
		if not self.window:
			self.window = DrawingWindow((self.canvas.width, self.canvas.height))
			print('window attached')
			
		image = NSImage.alloc().initWithSize_((self.canvas.width, self.canvas.height))
		image.lockFocus()

		# Walk objects
		for o in self.canvas.objects:
			output.extend(o.Generate(self))

		image.unlockFocus()
		self.window.w.image.setImage(imageObject=image)

		if not self.windowOpen:
			self.window.w.open()
		
		print('generated')
		


	def BezierPathBegin(self, o):
		
		self._NSBezierPath = NSBezierPath.bezierPath()
		return ['']

	def BezierPathEnd(self, o):

		# fill
		if o.fillcolor:
			NSColor.colorWithCalibratedRed_green_blue_alpha_(o.fillcolor.R, o.fillcolor.G, o.fillcolor.B, o.fillcolor.A).set()
			self._NSBezierPath.fill()

		# stroke
		if o.strokecolor:
			NSColor.colorWithCalibratedRed_green_blue_alpha_(o.strokecolor.R, o.strokecolor.G, o.strokecolor.B, o.strokecolor.A).set()
			self._NSBezierPath.setLineWidth_(o.strokewidth)
			self._NSBezierPath.stroke()

		return ['']

	def BezierPathMoveTo(self, o):
		self._NSBezierPath.moveToPoint_((o.x, o.y))
		return ['']
		
	def BezierPathLineTo(self, o):
		self._NSBezierPath.lineToPoint_((o.x, o.y))
		return ['']

	def BezierPathCurveTo(self, o):
		self._NSBezierPath.curveToPoint_controlPoint1_controlPoint2_((o.x3, o.y3), (o.x1, o.y1), (o.x2, o.y2))
		return ['']

	def BezierPathClosePath(self, o):
		self._NSBezierPath.closePath()
		return ['']

