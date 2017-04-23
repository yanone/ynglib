from AppKit import NSWindow, NSView, NSRect, NSPoint, NSColor, NSBezierPath, NSGraphicsContext, NSPrintInfo, NSPrintOperation, NSMutableData, NSTitledWindowMask, NSBackingStoreNonretained
#from AppKit import *
from base import BaseGeneratorDefinition

import os


class PDF(BaseGeneratorDefinition):
	def __init__(self, path):
		self.path = path
		self.registeredFonts = []
		self.Yfactor = 1.0
		

	def Generate(self):
		self.unit = 2.834645669291339

		self.pageRect = NSRect(NSPoint(0, 0), NSPoint(self.canvas.width * self.unit, self.canvas.height * self.unit))

		self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(self.pageRect, NSTitledWindowMask, NSBackingStoreNonretained, False)


		self.view = self.window.contentView()
#		self.view.setFrameOrigin_(self.pageRect.origin)
#		self.view.setFrameSize_(self.pageRect.size)
#		self.view.setNeedsDisplay_(False)


#		self.view = NSView.alloc().initWithFrame_(self.pageRect)
#		self.window.contentView().addSubview_(self.view)
		self.view.lockFocus()


#		self.printOperation = NSPrintOperation.PDFOperationWithView_insideRect_toPath_printInfo_(self.view, self.pageRect, self.path, NSPrintInfo)
#		self.printOperation.createContext()
#		print self.printOperation.context()
#		NSGraphicsContext.setCurrentContext_(self.printOperation.context())

		output = []

		# Walk objects
		for o in self.canvas.objects:
			output.extend(o.Generate(self))

		self.view.unlockFocus()

		# Write PDF		
		pdf = self.view.dataWithPDFInsideRect_(self.pageRect)
		pdf.writeToFile_atomically_(self.path, True)	

	def X(self, x):
		return x * self.unit

	def Y(self, y):
		return (self.canvas.height - y) * self.unit


	def setFillColor(self, color):
		if color.type == 'RGB':
			NSColor.colorWithDeviceRed_green_blue_alpha_(color.R/color.max, color.G/color.max, color.B/color.max, color.A * 100).set()
		elif color.type == 'CMYK':
			print 'fill CMYK'
			NSColor.colorWithDeviceCyan_magenta_yellow_black_alpha_(color.C/color.max, color.M/color.max, color.Y/color.max, color.K/color.max, color.A * 100).set()

	def setStrokeColor(self, color):
		if color.type == 'RGB':
			NSColor.colorWithDeviceRed_green_blue_alpha_(color.R/color.max, color.G/color.max, color.B/color.max, color.A * 100).set()
		elif color.type == 'CMYK':
			NSColor.colorWithDeviceCyan_magenta_yellow_black_alpha_(color.C/color.max, color.M/color.max, color.Y/color.max, color.K/color.max, color.A/color.max).set()


	def Rect(self, o):


		path = NSBezierPath.alloc().init()
#		path.appendBezierPathWithRoundedRect_xRadius_yRadius_(self.pageRect, 1, 1)
		#path.appendBezierPathWithRoundedRect_xRadius_yRadius_(NSRect(NSPoint(self.X(o.x), self.Y(o.y + o.height)), NSPoint(o.width * self.unit, o.height * self.unit)), 1, 1)
		path.appendBezierPathWithOvalInRect_(NSRect(NSPoint(self.X(o.x), self.Y(o.y + o.height)), NSPoint(o.width * self.unit, o.height * self.unit)))
		if o.fillcolor:
			self.setFillColor(o.fillcolor)
			path.fill()
		if o.strokecolor:
			self.setStrokeColor(o.fillcolor)
			path.stroke()

		return ['']
