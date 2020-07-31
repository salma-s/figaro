import TechDrawGui

class Exporter:
	def __init__(self, doc, savePath):
		self.doc = doc
		self.savePath = savePath

	def saveDrawings(self, shapeName):
		TechDrawGui.exportPageAsPdf(self.doc.getObject("Isometric"), '{}/{}-Isometric.pdf'.format(self.savePath, shapeName))
		TechDrawGui.exportPageAsPdf(self.doc.getObject("Orthographic"), '{}/{}-Orthographic.pdf'.format(self.savePath, shapeName))
