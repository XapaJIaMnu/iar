from math import floor, cos, sin
import numpy as np

map_file = open("map.txt", 'r')

map_array = [[0 for x in range(800)] for x in range(533)]
linenum = 0

for line in map_file:
    processed_line = line.split()
    processed_line = [int(x) for x in processed_line]
    map_array[linenum] = processed_line
    linenum = linenum + 1

def calcKatets(x, y, angl, dist):
    return (x-int(floor(sin(angl)*(41 + dist*15))), y+int(floor(cos(angl)*(41 + dist*15))))


class Map:
    def __init__(self, map):
        self.map_array = map

    def getNearbyWalls(self, x, y, phi):
        xx = x
        x = int(y) # TODO fix
        y = int(xx)
        map_array = self.map_array
        #map - 5 px = 1sm
        #robot diametur 5.5 sm., so we need 2.75*5 = 14 px radius
        ret_array = [] # [front, left, right

        # front
        found = False
        for i in range(1, 6):
            krow, kcol = calcKatets(x, y, phi, i)
            if krow >= 533 or kcol >= 800:
                ret_array.append(1)
                found = True
                break
            if (map_array[krow][kcol] == 1):
               ret_array.append(i)
               found = True
               break 
        if not found:
            ret_array.append(5)

        # left
        found = False
        for i in range(1, 6):
            krow, kcol = calcKatets(x, y, phi+np.pi/2, i)
            if krow >= 533 or kcol >= 800:
                ret_array.append(1)
                found = True
                break
            if (map_array[krow][kcol] == 1):
               ret_array.append(i)
               found = True
               break 
        if not found:
            ret_array.append(5)

        # right
        found = False
        for i in range(1, 6):
            krow, kcol = calcKatets(x, y, phi-np.pi/2, i)
            if krow >= 533 or kcol >= 800:
                ret_array.append(1)
                found = True
                break
            if (map_array[krow][kcol] == 1):
               ret_array.append(i)
               found = True
               break 
        if not found:
            ret_array.append(5)

        return ret_array
        #See if we have wall 1,2,3,4,5 sm in front of us
        #for i in range(1,6):
        #    katety = int(floor(cos(phi)/14 + i*5)) #14 pixels robot size + 55 pixels ahead of it 
        #    katetx = int(floor(sin(phi)/14 + i*5))
        #    if katetx+x > 799 or katety+y > 532:
        #        ret_array.append(i)
        #        break;

        #    print katetx + x
        #    print katety + y
        #    if (map_array[katetx + x][katety + y] == 1):
        #        ret_array.append(i)
        #        break;
        #    else:
        #        if (i == 5):
        #            #We haven't found a wall, return 0
        #            ret_array.append(0)
 
        #angl = phi+np.pi/2
        #self.mKatetsRight = calcKatets(x, y, angl, 6)

        ##See if we have wall 1,2,3,4,5 sm right of us
        #for i in range(1,6):
        #    katety = int(floor(cos(phi-np.pi)/14 + i*5)) #14 pixels robot size + 55 pixels ahead of it 
        #    katetx = int(floor(sin(phi-np.pi)/14 + i*5))
        #    if katetx+x > 799 or katety+y > 532:
        #        ret_array.append(i)
        #        break;

        #    if (map_array[katetx + x][katety + y] == 1):
        #        ret_array.append(i)
        #        break;
        #    else:
        #        if (i == 5):
        #            #We haven't found a wall, return 0
        #            ret_array.append(0)
 
        #angl = phi-np.pi/2

        #self.mKatetsLeft = calcKatets(x, y, angl, 6)

        ##See if we have wall 1,2,3,4,5 sm left of us
        #for i in range(1,6):
        #    katety = int(floor(cos(phi+np.pi)/14 + i*5)) #14 pixels robot size + 55 pixels ahead of it 
        #    katetx = int(floor(sin(phi+np.pi)/14 + i*5))
        #    if katetx+x > 799 or katety+y > 532:
        #        ret_array.append(i)
        #        break;

        #    if (map_array[katetx + x][katety + y] == 1):
        #        ret_array.append(i)
        #        break;
        #    else:
        #        if (i == 5):
        #            #We haven't found a wall, return 0
        #            ret_array.append(0)

        #return ret_array



def test():
    map_obj = Map(map_array)
    for i in range(800):
        for j in range(533):
            if map_obj.getNearbyWalls(i,j,0) != [0,0,0]:
                print "X is " + str(i) + " Y is " + str(j)
