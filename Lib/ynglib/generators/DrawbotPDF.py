# -*- coding: UTF-8 -*-

import sys
path = "/Applications/DrawBot.app/Contents/Resources/lib/python2.7/"
if path in sys.path:
	sys.path.remove(path)
sys.path.insert(0, path)
from drawBot import *
from drawBot.context.drawBotContext import DrawBotContext
from drawBot.context import getContextForFileExt


from base import BaseGeneratorDefinition
from ynglib.fonts import OpenTypeFont

import os


def OpenTypeFontInstall(self):
	if not self.installed:
		self.fontName = installFont(self.path)
OpenTypeFont.install = OpenTypeFontInstall


class PDF(BaseGeneratorDefinition):
	def __init__(self, path):
		self.path = path
		self.registeredFonts = []
		self.Yfactor = 1.0
		self.unit = 2.834645669291339
		

	def Generate(self):


		size(self.canvas.width * self.unit, self.canvas.height * self.unit)
		newDrawing()
		newPage(self.canvas.width * self.unit, self.canvas.height * self.unit)


		output = []

		# Walk objects
		for o in self.canvas.objects:
			output.extend(o.Generate(self))

		saveImage(self.path)

	def X(self, x):
		return x * self.unit

	def Y(self, y):
		return (self.canvas.height - y) * self.unit
#		return y * self.unit


	def setFillColor(self, color):
		if color.type == 'RGB':
			fill(color.R/color.max, color.G/color.max, color.B/color.max, color.A)
		elif color.type == 'CMYK':
			cmykFill(color.C/color.max, color.M/color.max, color.Y/color.max, color.K/color.max, color.A)

	def setStrokeColor(self, color):
		if color.type == 'RGB':
			stroke(color.R/color.max, color.G/color.max, color.B/color.max, color.A)
		elif color.type == 'CMYK':
			cmykStroke(color.C/color.max, color.M/color.max, color.Y/color.max, color.K/color.max, color.A)


	def TextArea(self, o):

		if o.fillcolor:
			self.setFillColor(o.fillcolor)
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)
			strokeWidth(o.strokewidth)
		else:
			strokeWidth(0)

		if o.lineheight:
			lineHeight(o.lineheight)
		else:
			lineHeight(o.fontsize)

		o.font.install()

		# OpenType features
		for feature in listOpenTypeFeatures(o.font.fontName):
			if feature in o.features:
				exec('openTypeFeatures(%s = True)' % feature)
			else:
				exec('openTypeFeatures(%s = False)' % feature)

		font(o.font.fontName, o.fontsize)
		textBox(o.text, (self.X(o.x), self.Y(o.y + o.height), o.width * self.unit, o.height * self.unit), align = o.align)

		return ['']





	def Text(self, o):

		if o.fillcolor:
			self.setFillColor(o.fillcolor)
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)
			strokeWidth(o.strokewidth)
		else:
			strokeWidth(0)



		o.font.install()

		# OpenType features
		for feature in listOpenTypeFeatures(o.font.fontName):
			if feature in o.features:
				exec('openTypeFeatures(%s = True)' % feature)
			else:
				exec('openTypeFeatures(%s = False)' % feature)

		font(o.font.fontName, o.fontsize)

		# Readjust alignment
		textBox('', (0, 0, 10, 10), align=o.align)


		text(o.text, (self.X(o.x), self.Y(o.y)))

		return ['']


	def Line(self, o):

		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)
		strokeWidth(o.strokewidth)

		strokeWidth(o.strokewidth)

		line((self.X(o.x1), self.Y(o.y1)), (self.X(o.x2), self.Y(o.y2)))

		return ['']


	def Ellipse(self, o):

		if o.fillcolor:
			self.setFillColor(o.fillcolor)
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)
			strokeWidth(o.strokewidth)
		else:
			strokeWidth(0)

		oval(self.X(o.x), self.Y(o.y + o.height), o.width * self.unit, o.height * self.unit)

		return ['']


	def Rect(self, o):

		if o.fillcolor:
			self.setFillColor(o.fillcolor)
		if o.strokecolor:
			self.setStrokeColor(o.strokecolor)
			strokeWidth(o.strokewidth)
		else:
			strokeWidth(0)

		strokeWidth(o.strokewidth)

		rect(self.X(o.x), self.Y(o.y + o.height), o.width * self.unit, o.height * self.unit)


		return ['']
