import TechDrawGui

class Exporter:
	def __init__(self, doc, savePath):
		self.doc = doc
		self.savePath = savePath

	def saveDrawings(self, shapeName):
		TechDrawGui.exportPageAsSvg(self.doc.getObject("Isometric"), '{}/{}-Isometric.svg'.format(self.savePath, shapeName))
		TechDrawGui.exportPageAsSvg(self.doc.getObject("Orthographic"), '{}/{}-Orthographic.svg'.format(self.savePath, shapeName))
