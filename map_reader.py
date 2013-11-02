from math import floor, cos, sin

map_file = open("map.txt", 'r')

map_array = [[0 for x in range(800)] for x in range(533)]
linenum = 0

for line in map_file:
    processed_line = line.split()
    processed_line = [int(x) for x in processed_line]
    map_array[linenum] = processed_line
    linenum = linenum + 1


def getNearbyWalls(x,y,phi):
    #map - 5 px = 1sm
    #robot diametur 5.5 sm., so we need 2.75*5 = 14 px radius
    ret_front = [] # [front1sm,front2sm,front3sm,front4sm,front5sm]
    ret_left = [] # [left1sm,left2sm,left3sm,left4sm,left5sm]
    ret_right = [] # [right1sm,right2sm,right3sm,right4sm,right5sm]

    #See if we have wall 1,2,3,4,5 sm in front of us
    for i in range(1,6):
        katety = int(floor(cos(phi)/14 + i*5)) #14 pixels robot size + 55 pixels ahead of it 
        katetx = int(floor(sin(phi)/14 + i*5))

        if (map_array[katetx][katety] == 1):
            ret_front.append(1)
        else:
            ret_front.append(0)

    #See if we have wall 1,2,3,4,5 sm right of us
    for i in range(1,6):
        katety = int(floor(cos(phi-90)/14 + i*5)) #14 pixels robot size + 55 pixels ahead of it 
        katetx = int(floor(sin(phi-90)/14 + i*5))

        if (map_array[katetx][katety] == 1):
            ret_right.append(1)
        else:
            ret_right.append(0)

    #See if we have wall 1,2,3,4,5 sm left of us
    for i in range(1,6):
        katety = int(floor(cos(phi-90)/14 + i*5)) #14 pixels robot size + 55 pixels ahead of it 
        katetx = int(floor(sin(phi-90)/14 + i*5))

        if (map_array[katetx][katety] == 1):
            ret_left.append(1)
        else:
            ret_left.append(0)

    return (ret_front, ret_right, ret_left)



    

