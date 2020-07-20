import TechDrawGui

class Exporter:
	def __init__(self, doc, savePath):
		self.doc = doc
		self.savePath = savePath

	def saveDrawings(self, shapeID):
		TechDrawGui.exportPageAsSvg(self.doc.getObject("Isometric"), '{}/{}-Isometric'.format(self.savePath, shapeID))
		TechDrawGui.exportPageAsSvg(self.doc.getObject("Orthographic"), '{}/{}-Orthographic'.format(self.savePath, shapeID))
