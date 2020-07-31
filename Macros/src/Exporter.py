import TechDrawGui

class Exporter:
	def __init__(self, doc, savePath):
		self.doc = doc
		self.savePath = savePath

	def saveDrawings(self, shapeName):
		TechDrawGui.exportPageAsPdf(self.doc.getObject("Isometric"), '{}/{}-Isometric'.format(self.savePath, shapeName))
		TechDrawGui.exportPageAsPdf(self.doc.getObject("Orthographic"), '{}/{}-Orthographic'.format(self.savePath, shapeName))
