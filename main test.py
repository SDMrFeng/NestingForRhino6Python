import rhinoscriptsyntax as rs
from createBoard import CreateBoard
from rectNestingOperation import RectNestingOperation
from getAllRectOutline import GetAllRectOutline
from returnObjectOutline import ReturnObjectOutline
from groupMove import GroupMove

rectOutlineList = [] # Outline list of bounding box for nesting
objects = [] # objects selected manually for nesting
rotatedAngle = [] # rotated angle for each object to fit in bounding box
objCenter = [] # object center for later group rotation and transformation
count = 0 # Count for number of objects include in nesting operation
movingCenter = [] # center of movement from object's original position
val = True # dummy for for-loop termination
nestingComplete = True

# create boards needed for nesting (default: 1220 (mm)*2440 (mm) boards with 20 (mm) safety (x50))
boards = CreateBoard(1220, 2440, 50, 20)
while val:
    count += 1
    temp = rs.GetObjects("Select objects needed to nest (Current obj count: %d)" % count, 0, True)
    if temp:
        objects.append(temp)
    else:
        break
# Ask user for safety distance between objects (I put 22 here not 20 for a reason)
objectSpacing = rs.GetReal("Please enter safety distance between objects (default 22 (mm)): ", 22, 0, 200)
objectSpacing /= 2
# find external contour for nesting operations
listOfObjOutlines = ReturnObjectOutline(objects)
# get min bounding box list (returned) and rotated angle for fitting
rectOutlineList = GetAllRectOutline(listOfObjOutlines,rotatedAngle,objCenter,movingCenter,objectSpacing)
# Nesting operation (core heuristic) (return true if objects to nest is more then boards)
nestingComplete = RectNestingOperation(boards, rectOutlineList)
# nesting completion validation
if (not nestingComplete):
    print("***** Nesting Operation Incomplete *****")
    print("(Could be Number of objects nesting is larger then number of board provided (adjust board count at main())")
    exit()
# Start moving in original objects
GroupMove(rectOutlineList, objects, objCenter, rotatedAngle, movingCenter)
# delete bounding box
rs.DeleteObjects(rectOutlineList)
print("***** Nesting operation Complete *****")

