import rhinoscriptsyntax as rs
from getMaxLength import GetMaxLength
from pointsReorder import PointsReorder
from System.Drawing import Color

def RectNestingOperation(boards, rectOutlineList):
    onBoard = [] # store the rectngles placed that are currently on this board
    rectInOrder = [] # store the rectangles that are in order
    curBoardIndex = 0 # number of board used
    nestingOrient = 1 # 1: current (big), 2: cur. turn 90 degrees, 3: reversed (small), 4: reversed and teuned 90 degrees 
    intersectWithRect = False
    
    # order rectangle by length (UPDATED)
    for i in rectOutlineList:
        # check if list is empty so far
        if len(rectInOrder) == 0:
            rectInOrder.append(i)
            continue
        lastIndex = len(rectInOrder) - 1
        index = 1
        rs.ObjectColor(i, Color.Orange)
        maxLength = GetMaxLength(i)
        # compare first and last 
        if GetMaxLength(rectInOrder[0]) >= maxLength:
            rectInOrder.insert(0,i)
            continue
        elif GetMaxLength(rectInOrder[lastIndex]) <= maxLength:
            rectInOrder.append(i)
            continue
        # check within the ordered list
        while GetMaxLength(rectInOrder[index]) < maxLength:
            index += 1
        rectInOrder.insert(index, i)
    # reverse rectangle order to descending order
    rectInOrder.reverse()
    
    while curBoardIndex <= len(boards):
        # check if ascend of descend placement (adjust curRect also)
        if len(rectInOrder) == 0:
            # done nesting, no more in list
            return True
        # update board if previous board is full
        curBoard = boards[curBoardIndex]
        curBoardPt = rs.PolylineVertices(curBoard)
        # nesting Orient checking
        if nestingOrient == 1 or nestingOrient == 2:
            if nestingOrient == 1:
                curRectIndex = 0 
                curRect = rectInOrder[curRectIndex]
                curRectPt = rs.PolylineVertices(curRect)
            else:
                rs.RotateObject(curRect,(curRectPt[0] + curRectPt[2]) / 2, 90)
        elif nestingOrient == 3 or nestingOrient == 4:
            if nestingOrient == 3:
                curRectIndex = len(rectInOrder) - 1
                curRect = rectInOrder[curRectIndex]
                curRectPt = rs.PolylineVertices(curRect)
            else:
                rs.RotateObject(curRect,(curRectPt[0] + curRectPt[2]) / 2, 90)                
        rs.ObjectColor(curRect, Color.LightBlue)
        curRectPt = rs.PolylineVertices(curRect)
        curRectPt = PointsReorder(curRectPt, 1)
        """
        *******************************************************************************************************************
        # arrange all rect with long side in lateral (MOVE THIS TO GETRECT CLASS)-> THIS IS MOVED TO GETALLRECTOUTLINE CLASS
        # SO WE CAN SUPPOSE ALL RECT PASSING IN IS MAX LENGTH AT LATERAL DIRECTION
        *******************************************************************************************************************
        if nestingOrient == 1 or nestingOrient == 3:
            if rs.Distance(curRectPt[0], curRectPt[1]) > rs.Distance(curRectPt[1], curRectPt[2]):
                rs.RotateObject(curRect,(curRectPt[0] + curRectPt[2]) / 2, 90)
        """
        # remake points for curRectPt and move to board start
        curRectPt = rs.PolylineVertices(curRect)
        curRectPt = PointsReorder(curRectPt, 1)
        moveInBoard = rs.VectorCreate(curBoardPt[0],curRectPt[0])
        rs.MoveObject(curRect, moveInBoard)
        curRectPt = rs.PolylineVertices(curRect)
        curRectPt = PointsReorder(curRectPt, 1)
        # nesting movement
        if len(onBoard) == 0:
            onBoard.append(curRect)
            rectInOrder.pop(curRectIndex)
        else:
            while True:
                # check intersection with other rect.
                for check in onBoard:
                    # True means intersect, false means good to place if other condition pass
                    intersectWithRect = (rs.IsObjectInBox(curRect, rs.PolylineVertices(check), False))
                    if intersectWithRect == True:
                        break                                    
                # in board status
                overBoard = curRectPt[1][0] > curBoardPt[1][0]
                changeBoard = curRectPt[2][1] > curBoardPt[2][1]
                if (changeBoard and nestingOrient == 4):
                    # change board                    
                    curBoardIndex += 1
                    curBoard = boards[curBoardIndex]
                    del onBoard[:] # clearing onBoard for next board
                    nestingOrient = 1
                    # move back to original location
                    rs.MoveObject(curRect, -moveInBoard)
                    break  
                elif (changeBoard):
                    # first change orientation and see if it can still fit
                    if (nestingOrient == 1):
                        nestingOrient = 2
                        break
                    elif (nestingOrient == 2):
                        nestingOrient = 3
                        # move back to original location (not super ideal but can't think of anything else at this point Lol)
                        moveTemp = [0,-2000000,0]
                        rs.MoveObject(curRect, moveTemp)
                        rs.RotateObject(curRect, (curRectPt[0] + curRectPt[2]) / 2, -90)
                        break
                    elif (nestingOrient == 3):
                        nestingOrient = 4
                        break
                elif (overBoard):
                   # switch to new y (up 1 interval)
                    lateralMove = [(curBoardPt[0][0] - curRectPt[0][0]), 20, 0]
                    rs.MoveObject(curRect,lateralMove)
                    curRectPt = rs.PolylineVertices(curRect)
                    curRectPt = PointsReorder(curRectPt, 1)
                elif (intersectWithRect):
                    rs.MoveObject(curRect,[10,0,0])
                    curRectPt = rs.PolylineVertices(curRect)
                    curRectPt = PointsReorder(curRectPt, 1)
                else:
                    onBoard.append(curRect)
                    rectInOrder.pop(curRectIndex)
                    # reset nesting orient to descending if location is found
                    if nestingOrient == 2:
                        nestingOrient = 1
                    elif nestingOrient == 4:
                        nestingOrient = 3
                    break
    return False # meaning element is more than the board that can nest