from base import BaseGeneratorDefinition


import objc, sys
from AppKit import *

import pygame
pygame.init()

class DrawingWindow(object):

	def __init__(self, size):
		self.w = vanilla.Window(size)
		self.w.image = vanilla.ImageView((0, 0, size[0], size[1]))

class pygameWindow(BaseGeneratorDefinition):
	def __init__(self):
		self.screen = None
		self.windowOpen = False

	def Generate(self):
		output = []

		if not self.screen:
			self.screen = pygame.display.set_mode((self.canvas.width, self.canvas.height))
			pygame.display.set_caption("Pi Bounce")
		
		pygame.display.flip()
		print 'generated'


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
			self._NSBezierPath.stroke(o.strokewidth)

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

#		return ['path.curveto(%s, %s, %s, %s, %s, %s)' % (o.x1, -o.y1 + o.bezierpath.canvas.height, o.x2, -o.y2 + o.bezierpath.canvas.height, o.x3, -o.y3 + o.bezierpath.canvas.height)]

	def BezierPathClosePath(self, o):
		self._NSBezierPath.closePath()
		return ['']

