import mountaincar
from Tilecoder import numTilings, numTiles, tilecode
from pylab import *  # includes numpy

numRuns = 1
# numTiles: 4*4*9
n = numTiles * 3 # number of components
gamma = 1

'''
    repeat for each episode:
        init S
        repeat for each step:
            choose the e-greedy action
            fill the features phi
            perform action, observe R,S'
            add R to G

            if S' is terminal:
                update theta1 & theta2
                break
            else if S' is not terminal:
                choose the greedy action, wrt the q of S',A': 
                    for each possible A', find q, choose the A' with the greatest q
                update theta1&theta2, using phi, newPhi
            S = S'
'''


def learn(alpha=.1/numTilings, epsilon=0, numEpisodes=200):
    theta1 = -0.001*rand(n)
    theta2 = -0.001*rand(n)
    returnSum = 0.0
    for episodeNum in range(numEpisodes):
        G = 0.0
        state = mountaincar.init() # S[0] is the position, S[1] is the velocity
        start = True
        step = 0
        while True:
            #print('$'*80)
            #print('new state: ', state)
            q1 = [0]*3 # for each possible actions, each has a q value
            q2 = [0]*3
            phi = [0]*n # initialize the list of features ø
            tileIndices = [-1]*numTilings
            tilecode(state[0], state[1], tileIndices)
            #print('tileIndices: ', tileIndices)

            # choose action, from a epsilon greedy
            num=np.random.random()
            if (num>=epsilon):
                for possibleAction in range(0,3):
                    # generate q value for each possible actions
                    for index in tileIndices: # implementing the vector multiplication thetaT*phi
                        q1[possibleAction] = q1[possibleAction] + theta1[possibleAction*numTiles+index]*1
                        q2[possibleAction] = q2[possibleAction] + theta2[possibleAction*numTiles+index]*1
                action = argmax([a+b for a, b in zip(q1, q2)]) # choose the greedy action
                #print('action is: ', action)
            else:
                action = np.random.randint(0,3) # choose the stochastic action

            #print('action is: ', action)
            # actually generate the features, based on the action
            indices = [action*numTiles+index for index in tileIndices] # indicates which position in phi is 1
            #print('indices: ', indices)
            # generating features, based on the action chosen in this state
            for index in indices:
                phi[index] = 1 # phi vector is generated for this state-action pair

            # sample the next state, reward
            reward, nextState = mountaincar.sample(state, action)
            #print('nextState:', nextState)
            #print('reward: ',reward)
            G = G+reward
            step+=1
            #print('G:', G)

            if nextState==None:
                # terminal state
                # theta1 = theta1 + alpha*(reward-theta1)*phi
                # theta2 = theta2 + alpha*(reward-theta2)*phi
                #nextState = (0,0)
                if np.random.randint(0,2):
                    for i in indices:
                        theta1[i] = theta1[i] + alpha*(reward - q1[action])
                else:
                    for i in indices:
                        theta2[i] = theta2[i] + alpha*(reward - q2[action])
                break
            else:
                # not terminal state
                # need to compute phi for the next state
                nextQ1 = [0]*3
                nextQ2 = [0]*3
                nextPhi = [0]*n
                nextTileIndices = [-1]*numTilings
                tilecode(nextState[0], nextState[1], nextTileIndices)
                #print('nextTileIndices: ', nextTileIndices)

                # generating features, based on the action chosen in this state
                #for index in nextIndices:
                #    nexetPhi[index] = 1 # phi vector is generated for this state-action pair

                if np.random.randint(0,2): # with 0.5 probability
                    #theta1 = theta1 + alpha*(reward + gamma*product(theta2, nextPhi, nextIndices) - theta1)*phi
                    #print(len(theta1))
                    #print(alpha)
                    # print(gamma*nextQ2[nextAction])
                    # print(len(phi))
                    # print(q1[action])
                    # print(alpha*(reward + gamma*nextQ2[nextAction] - q1[action]))
                    # print(type(phi))
                    # next action is always greedy
                    '''
                    for action in range(0,3):
                        # generate q value for each possible actions
                        for index in nextTileIndices: # implementing the vector multiplication thetaT*phi
                            nextQ1[action] = nextQ1[action] + theta1[action*numTiles+index]
                    '''
                    nextQ2 = Qs(nextTileIndices, theta2)
                    #nextAction = argmax(nextQ1) # choose the greedy action
                    #print('greedy action is: ', nextAction)
                     # indicates which position in phi is 1
                    #nextIndices = [nextAction*numTiles+index for index in nextTileIndices]
                    #print(nextIndices)
                    for i in indices:
                        theta1[i] = theta1[i] + alpha*(reward+max(nextQ2)-q1[action])
                    #print(theta1)
                    #error = alpha*(reward + gamma*nextQ2[nextAction] - q1[action])
                    #delta = [error*c for c in phi]
                    #theta1 = [a+b for a,b in zip(theta1,delta)]
                else:  # with 0.5 probability
                    #error = alpha*(reward + gamma*nextQ1[nextAction] - q2[action])
                    #delta = [error*c for c in phi]
                    #theta2 = [a+b for a,b in zip(theta2,delta)]

                    # next action is always greedy
                    '''
                    for action in range(0,3):
                        # generate q value for each possible actions
                        for index in nextTileIndices: # implementing the vector multiplication thetaT*phi
                            nextQ2[action] = nextQ2[action] + theta2[action*numTiles+index]
                    '''
                    nextQ1 = Qs(nextTileIndices, theta1)
                    #nextAction = argmax(nextQ2) # choose the greedy action
                    #print('greedy action is: ', nextAction)
                     # indicates which position in phi is 1
                    #nextIndices = [nextAction*numTiles+index for index in nextTileIndices]
                    #print(nextIndices)
                    for i in indices:
                        theta2[i] = theta2[i] + alpha*(reward+max(nextQ1)-q2[action])
                    #print(theta2)

            state = nextState
            #phi = nextPhi

        print("Episode: ", episodeNum, "Steps:", step, "Return: ", G)
        returnSum = returnSum + G
    print("Average return:", returnSum / numEpisodes)
    return returnSum, theta1, theta2

    
def Qs(tileIndices, theta):
    '''
    Write code to calculate the Q-values 
    for all actions for the state 
    represented by tileIndices
    '''    
    Q = [0]*3
    actions = [0,1,2]
    for a in range(len(actions)):
        for i in tileIndices:
            Q[a] = Q[a] + theta[i+(a*4*81)]
    return Q
#Additional code here to write average performance data to files for plotting...
#You will first need to add an array in which to collect the data


def writeF(theta1, theta2):
    fout = open('value', 'w')
    steps = 50
    for i in range(steps):
        for j in range(steps):
            F = [-1] * numTilings
            tilecode(-1.2 + (i * 1.7 / steps), -0.07 + (j * 0.14 / steps), F)
            height = -max(Qs(F, theta1 + theta2 / 2))
            fout.write(repr(height) + ' ')
        fout.write('\n')
    fout.close()

if __name__ == '__main__':
    runSum = 0.0
    for run in range(numRuns):
        returnSum, theta1, theta2 = learn()
        runSum += returnSum
    print("Overall performance: Average sum of return per run:", end="")
    print(runSum / numRuns)

    #writeF(theta1, theta2)