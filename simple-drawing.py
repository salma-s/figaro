import FreeCAD
import Part
import Drawing
import shutil

def shape(doc):
	# Create three boxes and a cylinder
	doc.addObject("Part::Box","Box")
	doc.Box.Length=100.00
	doc.Box.Width=100.00
	doc.Box.Height=100.00
	

	doc.addObject("Part::Box","Box1")
	doc.Box1.Length=90.00
	doc.Box1.Width=40.00
	doc.Box1.Height=100.00
	

	doc.addObject("Part::Box","Box2")
	doc.Box2.Length=20.00
	doc.Box2.Width=85.00
	doc.Box2.Height=100.00
	

	doc.addObject("Part::Cylinder","Cylinder")
	doc.Cylinder.Radius=80.00
	doc.Cylinder.Height=100.00
	doc.Cylinder.Angle=360.00
	

	# Fuse two boxes and the cylinder
	doc.addObject("Part::Fuse","Fusion")
	doc.Fusion.Base = doc.Cylinder
	doc.Fusion.Tool = doc.Box1
	

	doc.addObject("Part::Fuse","Fusion1")
	doc.Fusion1.Base = doc.Box2
	doc.Fusion1.Tool = doc.Fusion
	

	# Cut the fused shapes from the first box
	doc.addObject("Part::Cut","Shape")
	doc.Shape.Base = doc.Box 
	doc.Shape.Tool = doc.Fusion1


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

def exportDrawing(path):
    drawingSVGPath = doc.Page.PageResult
    shutil.copyfile(drawingSVGPath, path)

def exportFreeCAD(doc, path):
    doc.saveAs(path)

doc = FreeCAD.newDocument()
shape(doc)
draw(doc)
doc.recompute()

exportDrawing('./Output/output.svg')
exportFreeCAD(doc, './Output/output.FCStd')
