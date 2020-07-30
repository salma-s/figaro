import TechDrawGui

class Exporter:
	def __init__(self, doc, savePath):
		self.doc = doc
		self.savePath = savePath

	def saveDrawings(self, shapeID):
		TechDrawGui.exportPageAsPdf(self.doc.getObject("Isometric"), '{}/{}-Isometric'.format(self.savePath, shapeID))
		TechDrawGui.exportPageAsPdf(self.doc.getObject("Orthographic"), '{}/{}-Orthographic'.format(self.savePath, shapeID))
