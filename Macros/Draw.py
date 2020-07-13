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
        doc.ViewIso.X = 300.0
        doc.ViewIso.Y = 420.0
        doc.ViewIso.Scale = 1
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
        doc.FrontView.Y = 100.0
        doc.FrontView.Scale = 1
        doc.FrontView.Rotation = 0.0

        # Create a second view on the same object but this time the view is rotated by 90 degrees.
        # Right View
        rightView = doc.addObject('TechDraw::DrawViewPart','RightView')
        page2.addView(rightView)
        doc.RightView.Source = [shape]    
        doc.RightView.HardHidden=True
        doc.RightView.Direction = (1.0,0.0,0.0)
        doc.RightView.X = 580.0
        doc.RightView.Y = 100.0
        doc.RightView.Scale = 1
        doc.RightView.Rotation = 0.0

        # Create a second view on the same object but this time the view is rotated by 90 degrees.
        # Top View
        topView = doc.addObject('TechDraw::DrawViewPart','TopView')
        page2.addView(topView)
        doc.TopView.Source = [shape]
        doc.TopView.HardHidden=True
        doc.TopView.Direction = (0.0,0.0,1.0)
        doc.TopView.X = 100.0
        doc.TopView.Y = 400.0
        doc.TopView.Scale = 1
        doc.TopView.Rotation = 0.0
    
    @staticmethod
    def drawCentreline(doc, node, matrixX, matrixY, matrixZ, unit):
        style = 4
        weight = 0.6
        darkGrey = (1.0, 0.0, 0.0, 0.0)

        centrelineInfo = node.shape.centrelineInfo
        posXTrans = node.x * unit
        posYTrans = node.y * unit
        posZTrans = node.z * unit

        matrixXTrans = matrixX * unit / 2 - posXTrans
        matrixYTrans = matrixY * unit / 2 - posYTrans
        matrixZTrans = matrixZ * unit / 2 - posZTrans

        dvp = doc.FrontView
        if centrelineInfo.y is None:
            start = FreeCAD.Vector (centrelineInfo.x - centrelineInfo.centreArcLen - matrixXTrans, centrelineInfo.z - matrixZTrans, 0.0)
            end = FreeCAD.Vector(centrelineInfo.x + centrelineInfo.centreArcLen - matrixXTrans, centrelineInfo.z - matrixZTrans, 0.0)
            dvp.makeCosmeticLine(start, end, style, weight, darkGrey)
            start = FreeCAD.Vector (centrelineInfo.x - matrixXTrans, centrelineInfo.z - centrelineInfo.centreArcLen - matrixZTrans, 0.0)
            end = FreeCAD.Vector(centrelineInfo.x - matrixXTrans, centrelineInfo.z + centrelineInfo.centreArcLen - matrixZTrans, 0.0)
            dvp.makeCosmeticLine(start, end, style, weight, darkGrey)
        else:
            if centrelineInfo.x is None:
                start = FreeCAD.Vector (centrelineInfo.start - matrixXTrans, centrelineInfo.z - matrixZTrans, 0.0)
                end = FreeCAD.Vector(centrelineInfo.end - matrixXTrans, centrelineInfo.z - matrixZTrans, 0.0)
            elif centrelineInfo.z is None:
                start = FreeCAD.Vector (centrelineInfo.x - matrixXTrans, centrelineInfo.start - matrixZTrans, 0.0)
                end = FreeCAD.Vector(centrelineInfo.x - matrixXTrans, centrelineInfo.end - matrixZTrans, 0.0)  
            dvp.makeCosmeticLine(start, end, style, weight, darkGrey)


        dvp = doc.RightView
        if centrelineInfo.x is None:
            start = FreeCAD.Vector (centrelineInfo.y - centrelineInfo.centreArcLen - matrixYTrans, centrelineInfo.z - matrixZTrans, 0.0)
            end = FreeCAD.Vector(centrelineInfo.y + centrelineInfo.centreArcLen - matrixYTrans, centrelineInfo.z - matrixZTrans, 0.0)
            dvp.makeCosmeticLine(start, end, style, weight, darkGrey)
            start = FreeCAD.Vector (centrelineInfo.y - matrixYTrans, centrelineInfo.z - centrelineInfo.centreArcLen - matrixZTrans, 0.0)
            end = FreeCAD.Vector(centrelineInfo.y - matrixYTrans, centrelineInfo.z + centrelineInfo.centreArcLen - matrixZTrans, 0.0)
            dvp.makeCosmeticLine(start, end, style, weight, darkGrey)
        else:
            if centrelineInfo.y is None:
                start = FreeCAD.Vector (centrelineInfo.start - matrixYTrans, centrelineInfo.z - matrixZTrans, 0.0)
                end = FreeCAD.Vector(centrelineInfo.end - matrixYTrans, centrelineInfo.z - matrixZTrans, 0.0)
            elif centrelineInfo.z is None:
                start = FreeCAD.Vector (centrelineInfo.y - matrixYTrans, centrelineInfo.start - matrixZTrans, 0.0)
                end = FreeCAD.Vector(centrelineInfo.y - matrixYTrans, centrelineInfo.end - matrixZTrans, 0.0)  
            dvp.makeCosmeticLine(start, end, style, weight, darkGrey)


        dvp = doc.TopView
        if centrelineInfo.z is None:
            start = FreeCAD.Vector (centrelineInfo.x - centrelineInfo.centreArcLen - matrixXTrans, centrelineInfo.y - matrixYTrans, 0.0)
            end = FreeCAD.Vector(centrelineInfo.x + centrelineInfo.centreArcLen - matrixXTrans, centrelineInfo.y - matrixYTrans, 0.0)
            dvp.makeCosmeticLine(start, end, style, weight, darkGrey)
            start = FreeCAD.Vector (centrelineInfo.x - matrixXTrans, centrelineInfo.y - centrelineInfo.centreArcLen - matrixYTrans, 0.0)
            end = FreeCAD.Vector(centrelineInfo.x - matrixXTrans, centrelineInfo.y + centrelineInfo.centreArcLen - matrixYTrans, 0.0)
            dvp.makeCosmeticLine(start, end, style, weight, darkGrey)
        else:
            if centrelineInfo.x is None:
                start = FreeCAD.Vector (centrelineInfo.start - matrixXTrans, centrelineInfo.y - matrixYTrans, 0.0)
                end = FreeCAD.Vector(centrelineInfo.end - matrixXTrans, centrelineInfo.y - matrixYTrans, 0.0)
            elif centrelineInfo.y is None:
                start = FreeCAD.Vector (centrelineInfo.x - matrixXTrans, centrelineInfo.start - matrixYTrans, 0.0)
                end = FreeCAD.Vector(centrelineInfo.x - matrixXTrans, centrelineInfo.end - matrixYTrans, 0.0)  
            dvp.makeCosmeticLine(start, end, style, weight, darkGrey)
            