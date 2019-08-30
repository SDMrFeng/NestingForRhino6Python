import rhinoscriptsyntax as rs
from System.Drawing import Color
from pointsReorder import PointsReorder

# tranform group of objects together
def GroupMove(rectOutlineList, objects, objCenter, rotatedAngle, movingCenter):
    for objs, rect, center, rotAngle, centerStart in zip(objects, rectOutlineList, objCenter, rotatedAngle, movingCenter):         
        # rotate everything by center with rotatedAngle
        rs.RotateObjects(objs, center, rotAngle)
        # find vector to move from obj location to rectangle(obj center to rect center)
        boxCenter = rs.CurveAreaCentroid(rect)[0]
        moveVector = rs.VectorCreate(boxCenter, center)
        # check if object is in box
        rectPt = rs.PolylineVertices(rect)
        rectPt = PointsReorder(rectPt, 1)
        if rs.Distance(rectPt[0], rectPt[1]) > rs.Distance(rectPt[1], rectPt[2]):
            rs.RotateObjects(objs, center, 90)
        rs.MoveObjects(objs, moveVector)      