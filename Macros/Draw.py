from Node import Node
import TechDraw
import FreeCAD

class Draw:
    def __init__(self, doc, templatePath, shapeID):
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
        doc.ViewIso.Direction = (1.0,-1.0,1.0)
        doc.ViewIso.X = 120.0
        doc.ViewIso.Y = 150.0
        doc.ViewIso.Scale = 0.3
        doc.ViewIso.Rotation = 0.0
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
        doc.FrontView.Scale = 0.3
        doc.FrontView.Rotation = 0.0

        # Create a second view on the same object but this time the view is rotated by 90 degrees.
        # Right View
        rightView = doc.addObject('TechDraw::DrawViewPart','RightView')
        page2.addView(rightView)
        doc.RightView.Source = [shape]    
        doc.RightView.HardHidden=True
        doc.RightView.Direction = (1.0,0.0,0.0)
        doc.RightView.X = 200.0
        doc.RightView.Y = 120.0
        doc.RightView.Scale = 0.3
        doc.RightView.Rotation = 00.0

        # Create a second view on the same object but this time the view is rotated by 90 degrees.
        # Top View
        topView = doc.addObject('TechDraw::DrawViewPart','TopView')
        page2.addView(topView)
        doc.TopView.Source = [shape]
        doc.TopView.HardHidden=True
        doc.TopView.Direction = (0.0,0.0,1.0)
        doc.TopView.X = 100.0
        doc.TopView.Y = 230.0
        doc.TopView.Scale = 0.3
        doc.TopView.Rotation = 0.0
    
    @staticmethod
    def drawCentreline(doc, centrelineInfo):
            style = 4
            weight = 0.35
            darkGrey = (50.0, 50.0, 50.0, 1.0)

            dvp = doc.FrontView
            start = FreeCAD.Vector (0.0, 55.0, 0.0)
            end = FreeCAD.Vector(0.0, -55.0, 0.0)
            dvp.makeCosmeticLine(start,end,style, weight, darkGrey)


            dvp = doc.RightView
            start = FreeCAD.Vector (0.0, 55.0, 0.0)
            end = FreeCAD.Vector(0.0, -55.0, 0.0)
            dvp.makeCosmeticLine(start,end,style, weight, darkGrey)


            dvp = doc.TopView
            start = FreeCAD.Vector (0.0, 55.0, 0.0)
            end = FreeCAD.Vector(0.0, -55.0, 0.0)
            dvp.makeCosmeticLine(start,end,style, weight, darkGrey)


            start = FreeCAD.Vector (100.0, 0.0, 0.0)
            end = FreeCAD.Vector (-55.0, 295.0, 0.0)
            dvp.makeCosmeticLine(start,end,style, weight, darkGrey)
            