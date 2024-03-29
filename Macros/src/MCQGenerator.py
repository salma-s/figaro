import FreeCAD
import copy
import random
from ShapeGenerator import ShapeGenerator
from Node import Node
from Cuboid import *
from HoleInDoor import *
from HoleInBox import *
from HoleInWedge import *
from Wedge import *
from QuarterCircle import *
from QuarterHoleInCuboid import *
from SemiCircle import *
from SemiHoleInCuboid import *

class MCQGenerator:
    # Arguments
    # - map [dict]: The map of hashed coordinates to base shapes [Node] to deep copy
    # - doc: The FreeCAD document to create the deep copy in
    # Given a map of hashed coordinates [String] to base shapes [Node], create a deep copy of the map in a specified FreeCAD doc
    def mapDeepCopy(self, map, doc):
        mapCopy = {}
        for key in map.keys():
            # Deep copy the Shape stored in the Node
            node = map[key]
            shape = node.shape
            if shape == 'Empty':
                shapeCopy = 'Empty'
            elif shape != None:
                shapeCopy = shape.deepCopy(doc)

            # Deep copy the Node
            nodeCopy = Node(node.x, node.y, node.z, shapeCopy)
            mapCopy[key] = nodeCopy
        
        return mapCopy

    # Arguments
    # - shapeGenerator [ShapeGenerator]: The generator responsible for constructing the correct shape
    # - correctShapeMap [dict]: Maps the correct shapes corrdinates to base shapes
    # - distractorType [String]: Represents the SIMILAR/DISSIMILAR/DIFF_ROTATION type of the distractor(s) to generate in the MCQs
    def __init__(self, shapeGenerator, correctShapeMap, distractorType):
        # TODO: raise exception if type isnt SIMILAR/DISSIMILAR/DIFF_ROTATION
        self.shapeGenerator = shapeGenerator
        self.correctShapeMap = correctShapeMap
        self.distractorType = distractorType
        self.docs = [] #TODO: remove if not used
        self.baseShapeMaps = []
        self.shapeIDs = []
    
    def generateMutation(self, doc, shapeType, dimension, matrixPos, rotationIdx):
        if shapeType == 'Cuboid':
            return Cuboid(doc, dimension, matrixPos)
        elif shapeType == 'HoleInDoor':
            return HoleInDoor(doc, dimension, matrixPos, rotationIdx)
        elif shapeType == 'HoleInBox':
            return HoleInBox(doc, dimension, matrixPos, rotationIdx)
        elif shapeType == 'Wedge':
            return Wedge(doc, dimension, matrixPos, rotationIdx)
        elif shapeType == 'HoleInWedge':
            return HoleInWedge(doc, dimension, matrixPos, rotationIdx)
        elif shapeType == 'QuarterCircle':
            return QuarterCircle(doc, dimension, matrixPos, rotationIdx)
        elif shapeType == 'SemiCircle':
            return SemiCircle(doc, dimension, matrixPos, rotationIdx)  
        elif shapeType == 'QuarterHoleInCuboid':
            return QuarterHoleInCuboid(doc, dimension, matrixPos, rotationIdx)
        elif shapeType == 'SemiHoleInCuboid':
            return SemiHoleInCuboid(doc, dimension, matrixPos, rotationIdx)  
    
    # Returns the generated shape ID
    def generateShape(self, doc):
        mapCopy = self.mapDeepCopy(self.correctShapeMap, doc)

        # Get random coordinate to modify that base shape
        # TODO: for now, this can still generate the same base shape (possibly same rotation as well)   
        coordinatesList = list(mapCopy.keys())
        coordinateToRemove = ["0,1,0"] # Removes the block that can't be seen from the iso view
        coordinatesList = list(set(coordinatesList) - set(coordinateToRemove))
        randomCoordinate = coordinatesList[random.randint(0, len(coordinatesList) - 1)]
        baseShapeToChange = mapCopy[randomCoordinate]

        if self.distractorType == 'DIFF_ROTATION':
            # The random base shape cannot be Empty nor Cuboid since they cannot have a rotated to be a distractor
            while baseShapeToChange.shape == 'Empty' or baseShapeToChange.shape.baseShapeType == 'Cuboid':
                randomCoordinate = coordinatesList[random.randint(0, len(coordinatesList) - 1)]
                baseShapeToChange = mapCopy[randomCoordinate]
        else:
            # If the coordinate holds an empty shape, then choose another coordinate that holds a nonempty base shape
            # TODO: for now, if a shape is empty, it cannot have a distractor in place. would need an Empty base shape class
            # such that similar/dissimilar shapes can be retrieved
            while baseShapeToChange.shape == 'Empty':
                randomCoordinate = coordinatesList[random.randint(0, len(coordinatesList) - 1)]
                baseShapeToChange = mapCopy[randomCoordinate]

        # Remove the original shape from the FreeCAD document
        originalShape = mapCopy[randomCoordinate].shape
        doc.removeObject(originalShape.id)
        
        if self.distractorType == 'DISSIMILAR':
            # Create a dissimilar shape to the original
            [shapeType, rotationIdx] = originalShape.generateDissimilarShape(doc)
            distractorShape = self.generateMutation(doc, shapeType, originalShape.dimension, originalShape.matrixPos, rotationIdx)
        elif self.distractorType == 'SIMILAR':
            # Create a similiar shape to the original
            [shapeType, rotationIdx] = originalShape.generateSimilarShape(doc)
            distractorShape = self.generateMutation(doc, shapeType, originalShape.dimension, originalShape.matrixPos, rotationIdx)
        elif self.distractorType == 'DIFF_ROTATION':
            # Create the same original shape, but with a new rotation
            distractorShape = originalShape.deepCopyWithDifferentRotation(doc)
        
        mapCopy[randomCoordinate].shape = distractorShape 
        shapeID = self.shapeGenerator.generateShapeFromPredefinedMap(mapCopy, doc)
        
        self.shapeIDs.append(shapeID)
        self.docs.append(doc)
        self.baseShapeMaps.append(mapCopy)

        return shapeID