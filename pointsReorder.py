import rhinoscriptsyntax as rs

def PointsReorder(ptArr, op):
    option = op
    ordered = [0] * 5
    # Read Op order
    if option == 1:
        # find if array need reorder
        orig = 0
        for i in range(0,4):
            if round(ptArr[i][0]) <= round(ptArr[orig][0]) and round(ptArr[i][1]) <= round(ptArr[orig][1]):
                orig = i
        if orig == 0 or orig == 4:
            return ptArr
        else:
            # start rotating sequence
            for t in range(0,4):
                # new index to assign
                newIndex = (t + (4 - orig)) % 4
                ordered[newIndex] = ptArr[t]
            # concat first element back to last
            temp = ordered[0]
            ordered[4] = temp
            return ordered
    else:
        return False