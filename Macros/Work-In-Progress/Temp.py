from Node import Node
import TechDraw
import FreeCAD

class Draw:
    STYLE = 4
    WEIGHT = 0.6
    RED = (1.0, 0.0, 0.0, 0.0)

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
    def drawAllCentrelines(doc, node, matrixX, matrixY, matrixZ, unit):

        centrelineInfo = node.shape.centrelineInfo
        posXTrans = node.x * unit
        posYTrans = node.y * unit
        posZTrans = node.z * unit

        matrixXTrans = matrixX * unit / 2 - posXTrans
        matrixYTrans = matrixY * unit / 2 - posYTrans
        matrixZTrans = matrixZ * unit / 2 - posZTrans

        dvp = doc.FrontView
        if centrelineInfo.y is None:
            if centrelineInfo.centreArcInfo != None:
                Draw.drawUniqueCentreArcLine(dvp, centrelineInfo.centreArcInfo.line1, matrixXTrans, matrixZTrans)
                Draw.drawUniqueCentreArcLine(dvp, centrelineInfo.centreArcInfo.line2, matrixXTrans, matrixZTrans)
            else:
                Draw.drawGeneralCentreArc(dvp, centrelineInfo.x, matrixXTrans, centrelineInfo.z, matrixZTrans, centrelineInfo.centreArcLen)
        else:
            if centrelineInfo.x is None:
                Draw.drawHorizontalCentreline(dvp, centrelineInfo, matrixXTrans, centrelineInfo.z, matrixZTrans)
            elif centrelineInfo.z is None:
                Draw.drawVerticalCentreline(dvp, centrelineInfo.x, matrixXTrans, centrelineInfo, matrixZTrans)


        dvp = doc.RightView
        if centrelineInfo.x is None:
            if centrelineInfo.centreArcInfo != None:
                Draw.drawUniqueCentreArcLine(dvp, centrelineInfo.centreArcInfo.line1, matrixYTrans, matrixZTrans)
                Draw.drawUniqueCentreArcLine(dvp, centrelineInfo.centreArcInfo.line2, matrixYTrans, matrixXTrans)
            else:
                Draw.drawGeneralCentreArc(dvp, centrelineInfo.y, matrixYTrans, centrelineInfo.z, matrixZTrans, centrelineInfo.centreArcLen)
        else:
            if centrelineInfo.y is None:
                Draw.drawHorizontalCentreline(dvp, centrelineInfo, matrixYTrans, centrelineInfo.z, matrixZTrans)
            elif centrelineInfo.z is None:
                Draw.drawVerticalCentreline(dvp, centrelineInfo.y, matrixYTrans, centrelineInfo, matrixZTrans)


        dvp = doc.TopView
        if centrelineInfo.z is None:
            if centrelineInfo.centreArcInfo != None:
                Draw.drawUniqueCentreArcLine(dvp, centrelineInfo.centreArcInfo.line1, matrixXTrans, matrixYTrans)
                Draw.drawUniqueCentreArcLine(dvp, centrelineInfo.centreArcInfo.line2, matrixXTrans, matrixYTrans)
            else:
                Draw.drawGeneralCentreArc(dvp, centrelineInfo.x, matrixXTrans, centrelineInfo.y, matrixYTrans, centrelineInfo.centreArcLen)
        else:
            if centrelineInfo.x is None:
                Draw.drawHorizontalCentreline(dvp, centrelineInfo, matrixXTrans, centrelineInfo.y, matrixYTrans)
            elif centrelineInfo.y is None:
                Draw.drawVerticalCentreline(dvp, centrelineInfo.x, matrixXTrans, centrelineInfo, matrixYTrans)

    @staticmethod
    def drawUniqueCentreArcLine(dvp, centreArcInfoLine, centreXTrans, centreYTrans):
        start = FreeCAD.Vector(centreArcInfoLine[0] - centreXTrans, centreArcInfoLine[1] - centreYTrans, 0.0)
        end = FreeCAD.Vector(centreArcInfoLine[2] - centreXTrans, centreArcInfoLine[3] - centreYTrans, 0.0)
        dvp.makeCosmeticLine(start, end, Draw.STYLE, Draw.WEIGHT, Draw.RED)

    @staticmethod
    def drawGeneralCentreArc(dvp, x, centreXTrans, y, centreYTrans, arcLength):
        start = FreeCAD.Vector(x - arcLength - centreXTrans, y - centreYTrans, 0.0)
        end = FreeCAD.Vector(x + arcLength - centreXTrans, y - centreYTrans, 0.0)
        dvp.makeCosmeticLine(start, end, Draw.STYLE, Draw.WEIGHT, Draw.RED)
        start = FreeCAD.Vector(x - centreXTrans, y - arcLength - centreYTrans, 0.0)
        end = FreeCAD.Vector(x - centreXTrans, y + arcLength - centreYTrans, 0.0)
        dvp.makeCosmeticLine(start, end, Draw.STYLE, Draw.WEIGHT, Draw.RED)

    @staticmethod
    def drawHorizontalCentreline(dvp, centrelineInfo, centreXTrans, y, centreYTrans):
        start = FreeCAD.Vector (centrelineInfo.start - centreXTrans, y - centreYTrans, 0.0)
        end = FreeCAD.Vector(centrelineInfo.end - centreXTrans, y - centreYTrans, 0.0)
        dvp.makeCosmeticLine(start, end, Draw.STYLE, Draw.WEIGHT, Draw.RED)
    
    @staticmethod
    def drawVerticalCentreline(dvp, x, centreXTrans, centrelineInfo, centreYTrans):
        start = FreeCAD.Vector (x - centreXTrans, centrelineInfo.start - centreYTrans, 0.0)
        end = FreeCAD.Vector(x - centreXTrans, centrelineInfo.end - centreYTrans, 0.0)
        dvp.makeCosmeticLine(start, end, Draw.STYLE, Draw.WEIGHT, Draw.RED)
         