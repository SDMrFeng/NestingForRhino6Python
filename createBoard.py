import rhinoscriptsyntax as rs
from System.Drawing import Color

def CreateBoard(realWidth, realLength, count, sideSafety):
    boardCreated = [] # stores all board GUID in order
    spacing = 550 # unit in mm
    rowMax = 10
    width = realWidth - 2 * sideSafety
    length = realLength - 2 * sideSafety
    curPlane = rs.WorldXYPlane()
    # Create it's own board layer
    boardLayer = rs.AddLayer("Board Modified", Color.Red, True, True)
    rs.CurrentLayer(boardLayer)
    for i in range(0,count):
        localRowCount = i % rowMax
        localColCount = i // rowMax
        if localRowCount == 0 & localColCount != 0:
            localColCount -= 1
        tempBoard = rs.AddRectangle(curPlane,width,length)
        rs.MoveObject(tempBoard, ((width + spacing) * localRowCount, 
         (length + spacing) * localColCount, 0))
        boardCreated.append(tempBoard)
        del tempBoard
    # numbering for board created (can consider inside the for loop
    # of outside but addText works with either a point or plane.
    
    return boardCreated