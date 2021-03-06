import time, compositor



# store open files
compositorfontfiles = {}
maxcompositorfontfiles = 50


def CompositorFont(fontfilepath):
	import compositor
	from operator import itemgetter

	global compositorfontfiles

	# Sort
	sortedcompositorfontfiles = sorted(iter(compositorfontfiles.items()), key=itemgetter(1))
	
	if not fontfilepath in compositorfontfiles:
		compositorfontfiles[fontfilepath] = [time.time(), CompositorObject(fontfilepath)]

	# Set new timestamp
	compositorfontfiles[fontfilepath][0] = time.time()

	# Delete oldest objects
	while len(compositorfontfiles) > maxcompositorfontfiles:
#		compositorfontfiles.pop(sortedcompositorfontfiles.pop(0))
#		sortedcompositorfontfiles.pop(0)
		del compositorfontfiles[sortedcompositorfontfiles[0][0]]

	return compositorfontfiles[fontfilepath][1]


class Font:
	pass

class CompositorObject(Font):
	def __init__(self, path):
		self.path = path
		self.comp = compositor.Font(path)

class OpenTypeFont(Font):
	def __init__(self, path):
		self.path = path
		self.installed = False