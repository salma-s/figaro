import FreeCAD
import copy
import random
from ShapeGenerator import ShapeGenerator
from Node import Node

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
    # - numOfMCQs [Integer]: The number of MCQs to be generated, exclusive of the correct shape
    # - distractorDifficulty [String]: Represents the easy/medium/hard difficulty of the distractor(s) to generate in the MCQs
    def __init__(self, shapeGenerator, correctShapeMap, numOfMCQs, distractorDifficulty):
        #TODO: generate multiple docs
        #TODO: generate multiple mapo copies

        docs = []
        docs.append(FreeCAD.newDocument('copy'))
        doc = docs[0]
        mapCopy = self.mapDeepCopy(correctShapeMap, doc)
        
        self.docs = docs

        # Get random coordinate to modify that base shape
        # TODO: for now, this can still generate the same base shape (possibly same rotation as well)   
        coordinatesList = list(mapCopy.keys())
        randomCoordinate = coordinatesList[random.randint(0, len(coordinatesList) - 1)]
        baseShapeToChange = mapCopy[randomCoordinate]

        if distractorDifficulty == 'Hard':
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
        
        if distractorDifficulty == 'Easy':
            # Create a dissimilar shape to the original
            distractorShape = originalShape.generateDissimilarShape(doc)
            mapCopy[randomCoordinate].shape = distractorShape

        elif distractorDifficulty == 'Medium':
            # Create a similiar shape to the original
            distractorShape = originalShape.generateSimilarShape(doc)
            mapCopy[randomCoordinate].shape = distractorShape
        
        elif distractorDifficulty == 'Hard':
            # Create the same original shape, but with a new rotation
            distractorShape = originalShape.deepCopyWithDifferentRotation(doc)
            mapCopy[randomCoordinate].shape = distractorShape

        print('original map')
        for k in correctShapeMap.keys():
            if correctShapeMap[k].shape != 'Empty' and correctShapeMap[k].shape.baseShapeType != 'Cuboid':
                print(k + ' - ' + str(correctShapeMap[k].shape.rotationIndex))
        
        print('new map')
        for k in mapCopy.keys():
            if mapCopy[k].shape != 'Empty' and mapCopy[k].shape.baseShapeType != 'Cuboid':
                print(k + ' - ' + str(mapCopy[k].shape.rotationIndex))

        # Generate the shape with distractor(s) in the FreeCAD document
        self.finalShapeID = shapeGenerator.generateShapeFromPredefinedMap(mapCopy, doc)
        mcqMaps = []
        mcqMaps.append(mapCopy)
        self.mcqMaps = mcqMaps

    def getDoc(self):
        return self.docs[0]