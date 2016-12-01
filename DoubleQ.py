import blackjack
from pylab import *
import numpy as np

Q1=0.0000001*np.random.random((181,2)) # initialize the estimates
Q2=0.0000001*np.random.random((181,2)) # initialize the estimates

def learn(alpha, eps, numTrainingEpisodes):
    returnSum = 0.0
    gamma = 1.0
    for episodeNum in range(numTrainingEpisodes):
        G = 0
        state = blackjack.init()
        while(True):
            # choose action, from a epsilon greedy
            num=np.random.random()
            if (num>=eps):
                action = argmax(Q1[state]+Q2[state])
            else:
                action = np.random.randint(0,2)

            # perform action
            if state ==0:
                reward,nextState = blackjack.firstSample()
            else:
                reward,nextState = blackjack.sample(state,action)
            
            # to deal with the terminal state
            if nextState == False:
                nextState = 0

            if np.random.randint(0,2): # with 0.5 probability
                Q1[state][action]=Q1[state][action]+alpha*(reward+gamma*Q2[nextState][argmax(Q1[nextState])]-Q1[state][action])
            else:  # with 0.5 probability
                Q2[state][action]=Q2[state][action]+alpha*(reward+gamma*Q1[nextState][argmax(Q2[nextState])]-Q2[state][action])
            
            # update state
            state = nextState
            G = G + reward # update the return for state 0 with discount ratio gamma=1
                
            if state==False:
                break
        returnSum = returnSum + G
        if episodeNum % 10000 == 0 and episodeNum != 0:
            #print("Average return so far: ", returnSum / episodeNum)
            pass

            
def evaluate(numEvaluationEpisodes):
    returnSum = 0.0
    for episodeNum in range(numEvaluationEpisodes):
        G = 0
        state=blackjack.init()
        while(True):
            # choose the action greedy wrt the sum of two action values
            reward,state=blackjack.sample(state, argmax(Q1[state]+Q2[state]))
            G=G+reward

            if state==False:
                break
        returnSum = returnSum + G
    #print ("Determinstic return after learning: ",returnSum/numEvaluationEpisodes)

    return returnSum/numEvaluationEpisodes

def greedyAction(state):
    return argmax(Q1[state]+Q2[state])

if __name__ == "__main__":
    #epsilon = 1
    #main(epsilon, 10000)
    alpha = 0.001
    epsilon = 0.01
    learn(alpha, epsilon, 1000000)
    evaluate(1000000)
    #alpha = 0.0003
    #epsilon = 0.0125
    #learn(alpha, epsilon, 10000000)
    #evaluate(10000000)
    #blackjack.printPolicyToFile(greedyAction)