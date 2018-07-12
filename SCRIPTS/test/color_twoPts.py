import rhinoscriptsyntax as rs
from random import shuffle

def ColorObjsWithGradient():
    objs= rs.GetObjects("Select objects to color", preselect = True)
    if objs is None: return
    pt1 = rs.GetPoint("Select first color point")
    if pt1 is None: return
    firstColor = rs.GetColor()
    if firstColor is None: return
    pt2 = rs.GetPoint("Select second color point")
    if pt2 is None: return
    secondColor = rs.GetColor(firstColor)
    if secondColor is None: return
    
    rs.EnableRedraw(False)
    origLine = rs.AddLine(pt1, pt2)
    colorLine = rs.AddLine(firstColor, secondColor)
    
    
    for obj in objs:
        bboxpts = rs.BoundingBox(obj)
        ctrPt = (bboxpts[0] + bboxpts[6]) / 2
        param = rs.CurveClosestPoint(origLine, ctrPt)
        normParam = rs.CurveNormalizedParameter(origLine, param)
        colorParam = rs.CurveParameter(colorLine, normParam)
        finalPt = rs.EvaluateCurve(colorLine, colorParam)
        color = (finalPt.X, finalPt.Y, finalPt.Z)
        rs.ObjectColor(obj, color)    
    
    rs.DeleteObject(colorLine)
    rs.DeleteObject(origLine)
    rs.EnableRedraw(True)

def ColorObjsRandom():
    objs= rs.GetObjects("Select objects to color", preselect = True)
    if objs is None: return
    print "Select First Color"
    firstColor = rs.GetColor()
    if firstColor is None: return
    print "Select Second Color"
    secondColor = rs.GetColor(firstColor)
    if secondColor is None: return
    
    rs.EnableRedraw(False)
    colorLine = rs.AddLine(firstColor, secondColor)
    
    colors = rs.DivideCurve(colorLine, len(objs)-1)
    
    shuffle(colors)
    
    for i, obj in enumerate(objs):
        rs.ObjectColor(obj, (colors[i].X, colors[i].Y, colors[i].Z))    
    
    rs.DeleteObject(colorLine)
    rs.EnableRedraw(True)

if __name__ == "__main__":
    #func = rs.GetInteger("Input func number")
    func = 1
    if func == 0:
        ColorObjsWithGradient()
    elif func == 1:
        ColorObjsRandom()