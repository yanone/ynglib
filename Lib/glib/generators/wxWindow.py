from base import BaseGeneratorDefinition

from AppKit import *
import wx


class TestPanel(wx.Panel):
	def __init__(self, parent, log):
		self.log = log
		wx.Panel.__init__(self, parent, -1)

		self.Bind(wx.EVT_PAINT, self.OnPaint)

	def OnPaint(self, evt):
		dc = wx.PaintDC(self)
		gc = wx.GraphicsContext.Create(dc)

		font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
		font.SetWeight(wx.BOLD)
		gc.SetFont(font)

		# make a path that contains a circle and some lines, centered at 0,0
		path = gc.CreatePath()
		path.AddCircle(0, 0, BASE2)
		path.MoveToPoint(0, -BASE2)
		path.AddLineToPoint(0, BASE2)
		path.MoveToPoint(-BASE2, 0)
		path.AddLineToPoint(BASE2, 0)
		path.CloseSubpath()
		path.AddRectangle(-BASE4, -BASE4/2, BASE2, BASE4)


		# Now use that path to demonstrate various capbilites of the grpahics context
		gc.PushState()			 # save current translation/scale/other state 
		gc.Translate(60, 75)	   # reposition the context origin

		gc.SetPen(wx.Pen("navy", 1))
		gc.SetBrush(wx.Brush("pink"))
		gc.SetTextColour("black")

		# show the difference between stroking, filling and drawing
		for label, PathFunc in [("StrokePath", gc.StrokePath),
								("FillPath",   gc.FillPath),
								("DrawPath",   gc.DrawPath)]:
			if "wxGTK" in wx.PlatformInfo:
				w, h = dc.GetTextExtent(label) # NYI in Cairo context
			else:
				w, h = gc.GetTextExtent(label)

			gc.DrawText(label, -w/2, -BASE2-h)
			PathFunc(path)
			gc.Translate(2*BASE, 0)

			
		gc.PopState()			  # restore saved state
		gc.PushState()			 # save it again
		gc.Translate(60, 200)	  # offset to the lower part of the window
		
		gc.DrawText("Scale", 0, -BASE2)
		gc.Translate(0, 20)

		gc.SetBrush(wx.Brush(wx.Colour(178,  34,  34, 128)))   # 128 == half transparent
		for cnt in range(8):
			gc.Scale(1.08, 1.08)	# increase scale by 8%
			gc.Translate(5,5)	 
			gc.DrawPath(path)


		gc.PopState()			  # restore saved state
		gc.PushState()			 # save it again
		gc.Translate(400, 200)
		gc.DrawText("Rotate", 0, -BASE2)

		gc.Translate(0, 75)
		for angle in range(0, 360, 30):
			gc.PushState()		 # save this new current state so we can pop back to 
								   # it at the end of the loop
			r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(float(angle)/360, 1, 1)]
			gc.SetBrush(wx.Brush(wx.Colour(r, g, b, 64)))

			# use translate to artfully reposition each drawn path
			gc.Translate(1.5 * BASE2 * cos(radians(angle)),
						 1.5 * BASE2 * sin(radians(angle)))

			# use Rotate to rotate the path
			gc.Rotate(radians(angle))

			# now draw it
			gc.DrawPath(path)
			gc.PopState()

		gc.PopState()


class _wxFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=title, size=size)
		#self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		#self.canvas = wx.GraphicsContext()
		self.panel = TestPanel(self, None)



class wxWindow(BaseGeneratorDefinition):
	def __init__(self):
		self.wxapp = None

	def Generate(self):
		output = []

		# Initialize wx app
		if not self.wxapp:
			self.wxapp = wx.App(False)
			
#		image = NSImage.alloc().initWithSize_((self.canvas.width, self.canvas.height))
#		image.lockFocus()

		# Walk objects
#		for o in self.canvas.objects:
#			output.extend(o.Generate(self))

#		image.unlockFocus()
#		self.window.w.image.setImage(imageObject=image)
		
		self.wxFrame = _wxFrame(None, self.canvas.title, (self.canvas.width, self.canvas.height))
		self.wxFrame.Show(True)
		self.wxapp.MainLoop()


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

#		return ['path.curveto(%s, %s, %s, %s, %s, %s)' % (o.x1, -o.y1 + self.canvas.height, o.x2, -o.y2 + self.canvas.height, o.x3, -o.y3 + self.canvas.height)]

	def BezierPathClosePath(self, o):
		self._NSBezierPath.closePath()
		return ['']

