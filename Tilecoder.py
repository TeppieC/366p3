numTilings = 4
numTiles = numTilings*9*9

def tilecode(in1,in2,tileIndices):
    # write your tilecoder here (5 lines or so)
	for i in range(numTilings):
		newX = int((in1+1.2+0.2125/4*i)/0.2125)
		newY = int((in2+0.07+0.0175/4*i)/0.0175)
		tileIndices[i] = newX+newY*9+81*i
	return tileIndices

def printTileCoderIndices(in1,in2):
    tileIndices = [-1]*numTilings
    tilecode(in1,in2,tileIndices)
    #print('Tile indices for input (', in1, ',', in2,') are : ', tileIndices)

'''
if __name__ == '__main__':
    printTileCoderIndices(-1.2, -0.07)
    printTileCoderIndices(-1.2, 0.07)
    printTileCoderIndices(0.5, -0.07)
    printTileCoderIndices(0.5, 0.07)
    printTileCoderIndices(-0.35, 0.0)
    printTileCoderIndices(0.0, 0.0)
'''
