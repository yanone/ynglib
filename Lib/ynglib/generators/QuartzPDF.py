import Quartz as Q
import CoreGraphics as C
from AppKit import NSRect, NSPoint
from .base import BaseGeneratorDefinition

import os


class PDF(BaseGeneratorDefinition):
	def __init__(self, path):
		self.path = path
		self.registeredFonts = []
		self.Yfactor = 1.0
		

	def Generate(self):
		self.unit = 2.834645669291339

		self.pageRect = Q.CGRect(Q.CGPoint(0, 0), Q.CGPoint(self.canvas.width * self.unit, self.canvas.height * self.unit))

		url = Q.CFURLCreateWithFileSystemPath(None, self.path, Q.kCFURLPOSIXPathStyle, False)
		self.context = Q.CGPDFContextCreateWithURL(url, self.pageRect, None)

		Q.CGPDFContextBeginPage(self.context, None)

		output = []

		# Walk objects
		for o in self.canvas.objects:
			output.extend(o.Generate(self))

		Q.CGPDFContextEndPage(self.context)
		Q.CGContextRelease(self.context)	
		Q.CFRelease(url)

	def X(self, x):
		return x * self.unit

	def Y(self, y):
		return (self.canvas.height - y) * self.unit
#		return y * self.unit


	def setFillColor(self, color):
		if color.type == 'RGB':
			Q.CGContextSetFillColorWithColor(self.context, Q.CGColorCreateGenericRGB(color.R/color.max, color.G/color.max, color.B/color.max, color.A * 100))
		elif color.type == 'CMYK':
			Q.CGContextSetFillColorWithColor(self.context, Q.CGColorCreateGenericCMYK(color.C/color.max, color.M/color.max, color.Y/color.max, color.K/color.max, color.A * 100))

	def setStrokeColor(self, color):
		if color.type == 'RGB':
			Q.CGContextSetStrokeColorWithColor(self.context, Q.CGColorCreateGenericRGB(color.R/color.max, color.G/color.max, color.B/color.max, color.A * 100))
		elif color.type == 'CMYK':
			Q.CGContextSetStrokeColorWithColor(self.context, Q.CGColorCreateGenericCMYK(color.C/color.max, color.M/color.max, color.Y/color.max, color.K/color.max, color.A * 100))


	def Text(self, o):

		print(C.CTFontCreateWithName)


		attrString = Q.CFAttributedStringCreate(Q.kCFAllocatorDefault, o.text, {})
		line = Q.CTLineCreateWithAttributedString(attrString)
		Q.CGContextSetTextPosition(self.context, self.X(o.x), self.Y(o.y))
		Q.CTLineDraw(line, self.context)

		
		return ['']

		from reportlab.pdfbase import pdfmetrics
		from reportlab.pdfbase.ttfonts import TTFont
		if not os.path.basename(o.font) in self.registeredFonts:
			pdfmetrics.registerFont(TTFont(os.path.basename(o.font), o.font))
			self.registeredFonts.append(os.path.basename(o.font))

		if o.fillcolor:
			self.setFillColor(o.fillcolor)
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)

		self.reportlabcanvas.setFont(os.path.basename(o.font), o.fontsize)
		if o.align == 'left':
			self.reportlabcanvas.drawString(self.X(o.x), self.Y(o.y) - o.fontsize + .17*o.fontsize, o.text)
		elif o.align == 'center':
			self.reportlabcanvas.drawCentredString(self.X(o.x), self.Y(o.y) - o.fontsize + .17*o.fontsize, o.text)
		elif o.align == 'right':
			self.reportlabcanvas.drawRightString(self.X(o.x), self.Y(o.y) - o.fontsize + .17*o.fontsize, o.text)


		return ['']


	def Rect(self, o):

		if o.fillcolor:
			self.setFillColor(o.fillcolor)
			Q.CGContextFillRect(self.context, Q.CGRectMake(self.X(o.x), self.Y(o.y + o.height), o.width * self.unit, o.height * self.unit))

		if o.strokecolor:
			self.setStrokeColor(o.fillcolor)
			Q.CGContextStokeRect(self.context, Q.CGRectMake(self.X(o.x), self.Y(o.y), self.X(o.width), self.Y(o.height)))


		return ['']
