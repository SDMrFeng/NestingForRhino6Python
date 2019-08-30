import rhinoscriptsyntax as rs
from returnObjectOutline import ReturnObjectOutline
from System.Drawing import Color

def GetAllRectOutline(listOfObjOutlines,rotatedAngle,objCenter,movingCenter,objectSpacing):
    rectOutline = []
    for obj in listOfObjOutlines:
        counter = 1
        rotInterval = 1
        # create bounding box for rotInterval = 0
        lastBoxPt = rs.BoundingBox(obj)
        # CHANGE ROTCENTER TO OBJ CENTROID
        rotCenter = rs.CurveAreaCentroid(obj)[0]
        # append obj center into list
        objCenter.append(rotCenter)
        lastBoxArea = rs.Distance(lastBoxPt[1],lastBoxPt[0]) * rs.Distance(lastBoxPt[1],lastBoxPt[2])
        # making sure rotating toward min area.
        rs.RotateObject(obj,rotCenter,rotInterval)
        nxtBoxPt = rs.BoundingBox(obj)
        nxtBoxArea = rs.Distance(nxtBoxPt[0],nxtBoxPt[1]) * rs.Distance(nxtBoxPt[1],nxtBoxPt[2])
        # adjust rotation angle or store rectangle information if min
        if nxtBoxArea > lastBoxArea:
            rotInterval = -rotInterval
            rs.RotateObject(obj,rotCenter, (2*rotInterval))
            nxtBoxPt = rs.BoundingBox(obj)
            nxtBoxArea = rs.Distance(nxtBoxPt[0],nxtBoxPt[1]) * rs.Distance(nxtBoxPt[1],nxtBoxPt[2])
            if nxtBoxArea >= lastBoxArea:
                rs.RotateObject(obj,rotCenter,(-rotInterval) * counter)       
                lastBoxPt = lastBoxPt[:4]
                lastBoxPt.append(lastBoxPt[0])
                boxCenter = (lastBoxPt[0] + lastBoxPt[2]) / 2
                lastBox = rs.AddPolyline(lastBoxPt)
                # add safety between objects (20(mm) up and down)
                offsetBox = rs.OffsetCurve(lastBox, -boxCenter, objectSpacing)[0]
                rs.DeleteObject(lastBox)
                lastBox = offsetBox
                # check if max length is at lateral direction
                if rs.Distance(lastBoxPt[0], lastBoxPt[1]) > rs.Distance(lastBoxPt[1], lastBoxPt[2]):
                    rs.RotateObject(lastBox, boxCenter, 90)
                    # update angle turn
                    rotatedAngle.append(90)
                else:
                    # store angle turn without update
                    rotatedAngle.append(0)
                # Store GUID of each rectangle created
                rectOutline.append(lastBox)
                movingCenter.append(boxCenter)
                del lastBoxPt,lastBoxArea, nxtBoxPt, nxtBoxArea, offsetBox
                continue
        while nxtBoxArea <= lastBoxArea:
            counter += 1
            lastBoxPt = nxtBoxPt
            lastBoxArea = nxtBoxArea
            rs.RotateObject(obj,rotCenter,rotInterval)
            nxtBoxPt = rs.BoundingBox(obj)
            boxCenter = (lastBoxPt[0] + lastBoxPt[2]) / 2
            nxtBoxArea = rs.Distance(nxtBoxPt[0],nxtBoxPt[1]) * rs.Distance(nxtBoxPt[1],nxtBoxPt[2])
        # return curve back to original (zero) rotation
        rs.RotateObject(obj,rotCenter,(-rotInterval*counter))
        # Transform box pt to polyline
        lastBoxPt = lastBoxPt[:4]
        lastBoxPt.append(lastBoxPt[0])
        lastBox = rs.AddPolyline(lastBoxPt)
        # add safety between objects (20(mm) up and down)
        offsetBox = rs.OffsetCurve(lastBox, -boxCenter, objectSpacing)[0]
        rs.DeleteObject(lastBox)
        lastBox = offsetBox
        # check if max length is at lateral direction
        if rs.Distance(lastBoxPt[0], lastBoxPt[1]) > rs.Distance(lastBoxPt[1], lastBoxPt[2]):
            rs.RotateObject(lastBox,(lastBoxPt[0] + lastBoxPt[2]) / 2, 90)
            # update angle turn
            rotatedAngle.append(rotInterval * counter + 90)
        else:
            # store angle turn without update
            rotatedAngle.append(rotInterval * counter)
        # Store GUID of each rectangle created
        rectOutline.append(lastBox)
        movingCenter.append(boxCenter)
        del lastBoxPt,lastBoxArea, nxtBoxPt, nxtBoxArea, offsetBox
    # return List
    return rectOutline