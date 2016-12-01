import blackjack
from pylab import *
import numpy as np

def run(numEvaluationEpisodes):

    returnSum = 0.0
    for episodeNum in range(numEvaluationEpisodes): #loop for 2000 iterations
        G = 0
        state=blackjack.init()
        while(True): # if not reach the terminal state
            reward,state=blackjack.sample(state,np.random.randint(0,2))
            G=G+reward
            if state==False:
                break

        #print("Episode: ", episodeNum, "Return: ", G)
        returnSum = returnSum + G
    return returnSum/numEvaluationEpisodes

#numEvaluationEpisodes = 2000
#print("Average return: ", run(numEvaluationEpisodes))
