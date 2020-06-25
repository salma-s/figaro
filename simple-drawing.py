
import FreeCAD
import Part
import Drawing
import shutil

# -----------------------------------
#   Document Object IDs and Types
# -----------------------------------
boxes = []
cylinders = []
fusions = []
shapes = []

BOX = 'Box'
CYLINDER = 'Cylinder'
FUSION = 'Fusion'
SHAPE = 'Shape'

# Create id for the document object type and add it to the respective list
def generateID(objectType): 
	if objectType == BOX:
		id = BOX + str(len(boxes)+1 )
		boxes.append(id)
	elif objectType == CYLINDER:
		id = CYLINDER + str(len(cylinders)+1 )
		cylinders.append(id)
	elif objectType == FUSION:
		id = FUSION + str(len(fusions)+1 )
		fusions.append(id)
	return id


# -------------------------
#   Building Blocks
# -------------------------

# dimensions = [length, width, height]
def box(doc, id, dimensions):
	doc.addObject("Part::Box", id)
	doc.getObject(id).Length=dimensions[0]
	doc.getObject(id).Width=dimensions[1]
	doc.getObject(id).Height=dimensions[2]

# dimensions = [radius, height, angle]
def cylinder(doc, id, dimensions):
	doc.addObject("Part::Cylinder", id)
	doc.getObject(id).Radius=dimensions[0]
	doc.getObject(id).Height=dimensions[1]
	doc.getObject(id).Angle=dimensions[2]

# -------------------------
#   Fusion
# -------------------------

def fusePart(doc, fuseID, baseID, toolID):
	doc.addObject("Part::Fuse", fuseID)
	doc.getObject(fuseID).Base = doc.getObject(baseID)
	doc.getObject(fuseID).Tool = doc.getObject(toolID)

def fuseCut(doc, fuseID, baseID, toolID):
	doc.addObject("Part::Cut", fuseID)
	doc.getObject(fuseID).Base = doc.getObject(baseID)
	doc.getObject(fuseID).Tool = doc.getObject(toolID)

# -------------------------
#   Build Shape
# -------------------------

def shape(doc):
	# Create three boxes and a cylinder
	box(doc, generateID(BOX), [100, 100, 100])
	box(doc, generateID(BOX), [90, 40, 100])
	box(doc, generateID(BOX), [20, 85, 100])
	cylinder(doc, generateID(CYLINDER), [80, 100, 360])

	# Fuse two boxes and the cylinder
	fusePart(doc, generateID(FUSION), "Box2", "Cylinder1")
	fusePart(doc, generateID(FUSION), "Box3", "Fusion1")
	fuseCut(doc, "Shape", "Box1", "Fusion2")

def circularShape(doc): 
	box(doc, generateID(BOX), [100, 100, 100])
	cylinder(doc, generateID(CYLINDER), [40, 100, 360])

	doc.getObject("Cylinder1").Placement = FreeCAD.Placement(App.Vector(50,50,0), App.Rotation(0,0,0))	
	fuseCut(doc, "Shape", "Box1", "Cylinder1")

# -------------------------
#   Generate Drawings
# -------------------------

def draw(doc, templatePath, shapeID):
	shape = doc.getObject(shapeID)

	# Insert a Page object and assign a template
	page = doc.addObject('TechDraw::DrawPage', 'Isometric')
	template = doc.addObject('TechDraw::DrawSVGTemplate','Template')
	template.Template = templatePath
	page.Template = doc.Template
	
	# Create a third view on the same object but isometric view
	viewIso = doc.addObject('TechDraw::DrawViewPart','ViewIso')
	page.addView(viewIso)
	doc.ViewIso.Source = [shape]
	doc.ViewIso.Direction = (-1.0,-2.0,2.0)
	doc.ViewIso.X = 120.0
	doc.ViewIso.Y = 150.0
	doc.ViewIso.Scale = 1.20
	doc.ViewIso.Rotation = 108.5
	doc.ViewIso.HardHidden = False 
	
	# Insert a Page object and assign a template
	page2 = doc.addObject('TechDraw::DrawPage', 'Orthographic')
	page2.Template = FreeCAD.ActiveDocument.Template
	
	# Create a view on the Shape object, define the position and scale and assign it to a Page
	# Front View
	frontView = doc.addObject('TechDraw::DrawViewPart','FrontView')
	page2.addView(frontView)
	doc.FrontView.Source = [shape]
	doc.FrontView.HardHidden=True
	doc.FrontView.Direction = (0.0,-1.0,0.0)
	doc.FrontView.X = 100.0
	doc.FrontView.Y = 120.0
	doc.FrontView.Scale = 0.8
	doc.FrontView.Rotation = 90.0

	# Create a second view on the same object but this time the view is rotated by 90 degrees.
	# Right View
	rightView = doc.addObject('TechDraw::DrawViewPart','RightView')
	page2.addView(rightView)
	doc.RightView.Source = [shape]    
	doc.RightView.HardHidden=True
	doc.RightView.Direction = (0.0,0.0,1.0)
	doc.RightView.X = 230.0
	doc.RightView.Y = 120.0
	doc.RightView.Scale = 0.8
	doc.RightView.Rotation = 90.0

	# Create a second view on the same object but this time the view is rotated by 90 degrees.
	# Top View
	topView = doc.addObject('TechDraw::DrawViewPart','TopView')
	page2.addView(topView)
	doc.TopView.Source = [shape]
	doc.TopView.HardHidden=True
	doc.TopView.Direction = (-1.0,0.0,0.0)
	doc.TopView.X = 100.0
	doc.TopView.Y = 230.0
	doc.TopView.Scale = 0.8
	doc.TopView.Rotation = 90.0

# -------------------------
#   Exports
# -------------------------

# Will not work for macros

def exportDrawing(path):
    drawingSVGPath = doc.Page.PageResult
    shutil.copyfile(drawingSVGPath, path)

def exportFreeCAD(doc, path):
    doc.saveAs(path)

# -------------   Main    -------------

doc = FreeCAD.newDocument()
circularShape(doc)
draw(doc, 'Templates/A1_Landscape_plain.svg', "Shape")
doc.recompute()

exportDrawing('./Output/output.svg')
exportFreeCAD(doc, './Output/output.FCStd')
