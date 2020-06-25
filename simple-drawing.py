import FreeCAD
import Part
import Drawing
import shutil

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
	box(doc, "Box", [100, 100, 100])
	box(doc, "Box1", [90, 40, 100])
	box(doc, "Box2", [20, 85, 100])
	cylinder(doc, "Cylinder", [80, 100, 360])

	# Fuse two boxes and the cylinder
	fusePart(doc, "Fusion", "Box1", "Cylinder")
	fusePart(doc, "Fusion1", "Box2", "Fusion")
	fuseCut(doc, "Shape", "Box", "Fusion1")


# -------------------------
#   Generate Drawing
# -------------------------

def draw(doc):
	# Insert a Page object and assign a template
	doc.addObject('Drawing::FeaturePage','Page')
	doc.Page.Template = 'Templates/A1_Landscape_plain.svg'
	

	# Create a view on the Shape object, define the position and scale and assign it to a Page
	doc.addObject('Drawing::FeatureViewPart','View')
	doc.View.Source = doc.Shape
	doc.View.Direction = (0.0,0.0,1.0)
	doc.View.X = 10.0
	doc.View.Y = 10.0
	doc.Page.addObject(doc.View)
	

	# Create a second view on the same object but this time the view is rotated by 90 degrees.
	doc.addObject('Drawing::FeatureViewPart','ViewRot')
	doc.ViewRot.Source = doc.Shape
	doc.ViewRot.Direction = (0.0,0.0,1.0)
	doc.ViewRot.X = 290.0
	doc.ViewRot.Y = 30.0
	doc.ViewRot.Scale = 1.0
	doc.ViewRot.Rotation = 90.0
	doc.Page.addObject(doc.ViewRot)
	

	# Create a third view on the same object but isometric view
	doc.addObject('Drawing::FeatureViewPart','ViewIso')
	doc.ViewIso.Source = doc.Shape
	doc.ViewIso.Direction = (1.0,1.0,1.0)
	doc.ViewIso.X = 335.0
	doc.ViewIso.Y = 140.0
	doc.Page.addObject(doc.ViewIso)

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
shape(doc)
draw(doc)
doc.recompute()

exportDrawing('./Output/output.svg')
exportFreeCAD(doc, './Output/output.FCStd')
