import rhinoscriptsyntax as rs

# NOTE: "objects" are consider "unfiltered result of curve selection"
#       "listOfObjOutline" are consider "only the outline of the objects selected"
#
# return only the GUID of the external contour of the curve (listOfObjOutlines)
def ReturnObjectOutline(objects):
    listOfObjOutlines = []
    for id in objects: 
        for t in id:
            # check if closed curve
            if rs.IsCurveClosed(t):
                if rs.Area(t) > 1000:
                    listOfObjOutlines.append(t)
                    break
    return listOfObjOutlines