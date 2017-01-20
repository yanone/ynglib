# -*- coding: UTF-8 -*-

import sys, time
path = "/Applications/DrawBot.app/Contents/Resources/lib/python2.7/"
if path in sys.path:
	sys.path.remove(path)
sys.path.insert(0, path)

start = time.time()
from drawBot import *


from base import BaseGeneratorDefinition
from ynglib.fonts import OpenTypeFont
from ynlib.files import WriteToFile

import os



def OpenTypeFontInstall(self):
	if not self.installed:
		self.fontName = installFont(self.path)
		self.installed = True
		return ['installFont(\'' + self.path + '\')']
	else:
		return ['']
OpenTypeFont.install = OpenTypeFontInstall


class PDF(BaseGeneratorDefinition):
	def __init__(self, path):
		self.path = path
		self.registeredFonts = []
		self.Yfactor = 1.0
		self.unit = 2.834645669291339
		

	def Generate(self):


		output = []

		output.append('newPage(' + str(self.canvas.width * self.unit) + ', ' + str(self.canvas.height * self.unit) + ')')
		newPage(self.canvas.width * self.unit, self.canvas.height * self.unit)

		# Walk objects
		for o in self.canvas.objects:
			commands = o.Generate(self)
			if commands != ['']:
				output.extend(commands)

		output.append('endDrawing()')
		endDrawing()
		output.append('saveImage(\'' + self.path + '\')')
		saveImage(self.path)

		if False:
			for line in output:
				if not line.strip().startswith('#') and line.strip() != '':
					try:
						exec(line)
					except:
						print line

#		print '\n'.join(output)

	def X(self, x):
		return x * self.unit

	def Y(self, y):
		return (self.canvas.height - y) * self.unit
#		return y * self.unit


	def setFillColor(self, color):
		if color:
			if color.type == 'RGB':
				fill(color.R/color.max, color.G/color.max, color.B/color.max, color.A)
				return ['fill(' + str(color.R/color.max) + ', ' + str(color.G/color.max) + ', ' + str(color.B/color.max) + ', ' + str(color.A) + ')']
			elif color.type == 'CMYK':
				cmykFill(color.C/color.max, color.M/color.max, color.Y/color.max, color.K/color.max, color.A)
				return ['cmykFill(' + str(color.C/color.max) + ', ' + str(color.M/color.max) + ', ' + str(color.Y/color.max) + ', ' + str(color.K/color.max) + ', ' + str(color.A) + ')']
		else:
			fill(None)
			return ['fill(None)']

	def setStrokeColor(self, color):
		if color.type == 'RGB':
			stroke(color.R/color.max, color.G/color.max, color.B/color.max, color.A)
			return ['stroke(' + str(color.R/color.max) + ', ' + str(color.G/color.max) + ', ' + str(color.B/color.max) + ', ' + str(color.A) + ')']
		elif color.type == 'CMYK':
			cmykStroke(color.C/color.max, color.M/color.max, color.Y/color.max, color.K/color.max, color.A)
			return ['cmykStroke(' + str(color.C/color.max) + ', ' + str(color.M/color.max) + ', ' + str(color.Y/color.max) + ', ' + str(color.K/color.max) + ', ' + str(color.A) + ')']


	def setColors(self, o):
		
		commands = []

		if hasattr(o, 'fillcolor') and o.fillcolor:
			commands.extend(self.setFillColor(o.fillcolor))
		else:
			fill(None)
			commands.append('fill(None)')
		if o.strokecolor:
			commands.extend(self.setStrokeColor(o.strokecolor))
			strokeWidth(o.strokewidth)
			commands.append('strokeWidth(' + str(o.strokewidth) + ')')
		else:
			stroke(None)
			commands.append('stroke(None)')
			strokeWidth(None)
			commands.append('strokeWidth(None)')

		return commands

	def setFontStuff(self, o):

		commands = []

		if o.lineheight:
			lineHeight(o.lineheight)
			commands.append('lineHeight(' + str(o.lineheight) + ')')
		else:
			lineHeight(o.fontsize)
			commands.append('lineHeight(' + str(o.fontsize) + ')')

		commands.extend(o.font.install())

		# Font
		font(o.font.fontName)
		commands.append('font(\'' + str(o.font.fontName) + '\')')
		fontSize(o.fontsize)
		commands.append('fontSize(' + str(o.fontsize) + ')')

		# OpenType features ON
		features = {}
		for feature in listOpenTypeFeatures(o.font.fontName):
			if feature in o.features:
				features[feature] = True
			if feature in o.featuresOff:
				features[feature] = False

		if features.keys():
			call = 'openTypeFeatures(%s)' % ', '.join(['%s=%s' % (x, features[x]) for x in features])
			exec(call)
			commands.append(call)

		# Language
		if o.language:
			language(o.language)
			commands.append('language(\'' + str(o.language) + '\')')
		else:
			language(None)
			commands.append('language(None)')

		return commands

	def unsetFontStuff(self, o):

		commands = []

		# OpenType features OFF
		features = {}
		for feature in listOpenTypeFeatures(o.font.fontName):
			if feature in o.features:
				features[feature] = False
			if feature in o.featuresOff:
				features[feature] = True
		if features.keys():
			call = 'openTypeFeatures(%s)' % ', '.join(['%s=%s' % (x, features[x]) for x in features])
			exec(call)
			commands.append(call)

		return commands


	def TextArea(self, o):

		commands = []

		commands.extend(self.setColors(o))
		commands.extend(self.setFontStuff(o))

		textBox(o.text, (self.X(o.x), self.Y(o.y + o.height), o.width * self.unit, o.height * self.unit), align = o.align)
		commands.append('textBox(u\'\'\'' + o.text + '\'\'\', (' + str(self.X(o.x)) + ', ' + str(self.Y(o.y + o.height)) + ', ' + str(o.width * self.unit) + ', ' + str(o.height * self.unit) + '), align = \'' + o.align + '\')')

		commands.extend(self.unsetFontStuff(o))

		commands.append('\n########################\n')

		return commands





	def Text(self, o):

		commands = []

		commands.extend(self.setColors(o))
		commands.extend(self.setFontStuff(o))

		text(o.text, (self.X(o.x), self.Y(o.y)), align = o.align)
		commands.append('text(u\'\'\'' + o.text + '\'\'\', (' + str(self.X(o.x)) + ', ' + str(self.Y(o.y)) + '))')

		commands.extend(self.unsetFontStuff(o))

		commands.append('\n########################\n')

		return commands


	def Line(self, o):

		commands = []

		commands.extend(self.setColors(o))

		line((self.X(o.x1), self.Y(o.y1)), (self.X(o.x2), self.Y(o.y2)))
		commands.append('line((' + str(self.X(o.x1)) + ', ' + str(self.Y(o.y1)) + '), (' + str(self.X(o.x2)) + ', ' + str(self.Y(o.y2)) + '))')

		commands.append('\n########################\n')

		return commands


	def Ellipse(self, o):

		commands = []

		commands.extend(self.setColors(o))

		oval(self.X(o.x), self.Y(o.y + o.height), o.width * self.unit, o.height * self.unit)
		commands.append('oval(' + str(self.X(o.x)) + ', ' + str(self.Y(o.y + o.height)) + ', ' + str(o.width * self.unit) + ', ' + str(o.height * self.unit) + ')')

		commands.append('\n########################\n')

		return commands


	def Rect(self, o):

		commands = []

		commands.extend(self.setColors(o))

		rect(self.X(o.x), self.Y(o.y + o.height), o.width * self.unit, o.height * self.unit)
		commands.append('rect(' + str(self.X(o.x)) + ', ' + str(self.Y(o.y + o.height)) + ', ' + str(o.width * self.unit) + ', ' + str(o.height * self.unit) + ')')

		commands.append('\n########################\n')

		return commands

	def NewPage(self, o):
		newPage(self.canvas.width * self.unit, self.canvas.height * self.unit)
		return ['newPage(' + str(self.canvas.width * self.unit) + ', ' + str(self.canvas.height * self.unit) + ')']



	def BezierPathBegin(self, o):

		commands = []

		commands.extend(self.setColors(o))

		newPath()
		commands.append('newPath()')
		return commands

	def BezierPathEnd(self, o):
		drawPath()
		return ['drawPath()', '\n########################\n']

	def BezierPathMoveTo(self, o):
		moveTo((self.X(o.x), self.Y(o.y)))
		return ['moveTo((' + str(self.X(o.x)) + ', ' + str(self.Y(o.y)) + '))']

	def BezierPathLineTo(self, o):
		lineTo((self.X(o.x), self.Y(o.y)))
		return ['lineTo((' + str(self.X(o.x)) + ', ' + str(self.Y(o.y)) + '))']

	def BezierPathCurveTo(self, o):
		curveTo((self.X(o.x1), self.Y(o.y1)), (self.X(o.x2), self.Y(o.y2)), (self.X(o.x3), self.Y(o.y3)))
		return ['curveTo((' + str(self.X(o.x1)) + ', ' + str(self.Y(o.y1)) + '), (' + str(self.X(o.x2)) + ', ' + str(self.Y(o.y2)) + '), (' + str(self.X(o.x3)) + ', ' + str(self.Y(o.y3)) + '))']

	def BezierPathClosePath(self, o):
		closePath()
		return ['closePath()']

