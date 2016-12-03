numTilings = 4
numTiles = numTilings*9*9
    
def tilecode(in1,in2,tileIndices):
    # write your tilecoder here (5 lines or so)
	for i in range(numTilings):
		newX = int((in1+0.6/4*i)/0.6)
		newY = int((in2+0.6/4*i)/0.6)
		tileIndices[i] = newX+newY*9+81*i
	return tileIndices
    
def printTileCoderIndices(in1,in2):
    tileIndices = [-1]*numTilings
    tilecode(in1,in2,tileIndices)
    print('Tile indices for input (', in1, ',', in2,') are : ', tileIndices)
