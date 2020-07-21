from Node import Node
from BaseShapeFactory import BaseShapeFactory
import FreeCAD

class ShapeGenerator:
    # Converts the x, y, z coordinates of base shape into a String representation 'x,y,z'
    def hashCoordinates(self, x, y, z):
	    return '{},{},{}'.format(x, y, z)

    # Generate a unique ID for a shape which is a result of a fusion
    def generateFusionID(self): 
        id = 'Fusion' + str(len(self.fusionIDs)+1 )
        self.fusionIDs.append(id)
        return id

    # Fuse two shapes together using the FreeCAD fusion function
    def join(self, doc, base, new, unit):
        id = self.generateFusionID()
        doc.addObject("Part::Fuse", id)
        doc.getObject(id).Base = doc.getObject(base)
        doc.getObject(id).Tool = doc.getObject(new.shape.id)
        return id

    # doc: The current FreeCAD document object 
    # matrixX: [Integer] The number of units in the x dimension of the shape matrix
    # matrixY: [Integer] The number of units in the y dimension of the shape matrix
    # matrixZ: [Integer] The number of units in the z dimension of the shape matrix
    # unit: [Integer] The length of a single unit in the shape matrix
    def __init__(self, doc, matrixX, matrixY, matrixZ, unit):
        self.doc = doc
        self.matrixX = matrixX
        self.matrixY = matrixY
        self.matrixZ = matrixZ
        self.unit = unit
        self.reachableNodes = {'0,0,0'}

        # Stores the IDs of shapes which are a result of a fusion
        self.fusionIDs = []

        # Initialise the map of coordinates to base shape node units
        baseShapeMap = {}
        for i in range(0, self.matrixX):
            for j in range (0, self.matrixY):
                for k in range (0, self.matrixZ):
                    baseShapeMap[self.hashCoordinates(i, j, k)] = Node(i, j, k)
        
        self.baseShapeMap = baseShapeMap

    def checkReachability(self, nodeCoords):
        hashedString = self.hashCoordinates(nodeCoords[0], nodeCoords[1], nodeCoords[2])
        adjacentNode = self.baseShapeMap[hashedString]
        if adjacentNode.shape is None and adjacentNode.reachable is False:
            adjacentNode.reachable = True
            self.reachableNodes.add(hashedString)

    def relaxGraph(self, currentNode, reachableNodes):
        if currentNode.shape != "Empty":
            if currentNode.x != 0:
                self.checkReachability([currentNode.x - 1, currentNode.y, currentNode.z])
            if currentNode.x != self.matrixX - 1:
                self.checkReachability([currentNode.x + 1, currentNode.y, currentNode.z])
            if currentNode.y != 0:
                self.checkReachability([currentNode.x, currentNode.y - 1, currentNode.z])
            if currentNode.y != self.matrixY - 1:
                self.checkReachability([currentNode.x, currentNode.y + 1, currentNode.z])
            if currentNode.z != 0:		
                self.checkReachability([currentNode.x, currentNode.y, currentNode.z - 1])
            if currentNode.z != self.matrixZ - 1:
                self.checkReachability([currentNode.x, currentNode.y, currentNode.z + 1])	

    # The algorithm which generate a shape with a specified complexity
    def generate(self, complexity):
        shapeFactory = BaseShapeFactory(self.doc, self.unit, self.matrixX * self.matrixY * self.matrixZ, complexity)
        base = None

        while len(self.reachableNodes) != 0:
            nodeHash = self.reachableNodes.pop()
            currentNode = self.baseShapeMap[nodeHash]
            while currentNode.shape is None or self.baseShapeMap["0,0,0"].shape == "Empty":
                currentNode.shape = shapeFactory.generateRandomShape([currentNode.x, currentNode.y, currentNode.z])
            if base is None and currentNode.shape != "Empty":
                base = currentNode.shape.id
            elif currentNode.shape != "Empty":
                base = self.join(self.doc, base, currentNode, self.unit)
            currentNode.reachable = False
            self.relaxGraph(currentNode, self.reachableNodes)
        return base