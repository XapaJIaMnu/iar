import Image 

#Load image
im = Image.open("allblack.png")
pix = im.load()

#Container
map_array = [[0 for x in range(533)] for x in range(800)]

for j in range(533):
    for i in range(800):
        if sum(pix[i,j]) <= 40:
            map_array[i][j] = 1
        else:
            map_array[i][j] = 0

output = open("map.txt", 'w')
output_human = open("map_human.txt", 'w')

for i in reversed(range(len(map_array))):
    print >> output, str(map_array[i]).replace('[','').replace(']', '').replace(',', '')
    print >> output_human, str(map_array[i]).replace('[','').replace(']', '').replace(',', '').replace(' ','')

#for line in map_array:
#    print >> output, str(line).replace('[','').replace(']', '').replace(',', '')
#    print >> output_human, str(line).replace('[','').replace(']', '').replace(',', '').replace(' ','')

output.close

