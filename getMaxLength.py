import rhinoscriptsyntax as rs
from pointsReorder import PointsReorder
from System.Drawing import Color

# function specifically to return max length
def GetMaxLength(rect):
    # find long side
    rs.ObjectColor(rect, Color.Blue)
    tempPt = rs.PolylineVertices(rect)
    tempPt = PointsReorder(tempPt, 1)
    if rs.Distance(tempPt[0], tempPt[1]) > rs.Distance(tempPt[1], tempPt[2]):
        rs.ObjectColor(rect, Color.Orange)
        return rs.Distance(tempPt[0], tempPt[1])
    else:
        rs.ObjectColor(rect, Color.Orange)
        return rs.Distance(tempPt[1], tempPt[2])