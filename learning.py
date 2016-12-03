import mountaincar
from Tilecoder import numTilings, numTiles, tilecode
from pylab import *  # includes numpy

numRuns = 1
# numTiles: 4*4*9
n = numTiles * 3 # number of components
phi = [-1]*numTilings  # initialize the list of tileindices
gamma = 1

def learn(alpha=.1/numTilings, epsilon=0, numEpisodes=200):
    theta1 = -0.001*rand(n)
    theta2 = -0.001*rand(n)
    returnSum = 0.0
    for episodeNum in range(numEpisodes):
        G = 0
        S = mountaincar.init()

        while True:

            tilecode(S[0], S[1], phi)

            if np.random.randint(0,2): # with 0.5 probability
                theta1[state][action]=theta1[state][action]+alpha*(reward+gamma*theta2[nextState][argmax(theta1[nextState])]-theta1[state][action])
            else:  # with 0.5 probability
                theta2[state][action]=theta2[state][action]+alpha*(reward+gamma*theta1[nextState][argmax(theta2[nextState])]-theta2[state][action])
        
        print("Episode: ", episodeNum, "Steps:", step, "Return: ", G)
        returnSum = returnSum + G
    print("Average return:", returnSum / numEpisodes)
    return returnSum, theta1, theta2


#Additional code here to write average performance data to files for plotting...
#You will first need to add an array in which to collect the data

def writeF(theta1, theta2):
    fout = open('value', 'w')
    steps = 50
    for i in range(steps):
        for j in range(steps):
            F = tilecode(-1.2 + i * 1.7 / steps, -0.07 + j * 0.14 / steps)
            height = -max(Qs(F, theta1, theta2))
            fout.write(repr(height) + ' ')
        fout.write('\n')
    fout.close()


if __name__ == '__main__':
    runSum = 0.0
    for run in range(numRuns):
        returnSum, theta1, theta2 = learn()
        runSum += returnSum
    print("Overall performance: Average sum of return per run:", runSum/numRuns)
