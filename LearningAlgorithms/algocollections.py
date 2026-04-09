## HAS COLLECTION OF BASE CLASS AND ALL OTHER LEARNING ALGORITHMS

# Importing libraries
import abc
import collections
import numpy as np
import random as rd
# Base Algorithm class
class BaseLearner(abc.ABC):
    def __init__(self, size = 3, alpha = 0.5, gamma = 0.9, epsilon = 0.1) -> None:
        """
        Initializes a base learning agent with given values

        (Args)
            size : the size of the game (usually 3)
            alpha :  learning rate or step size parameter
            gamma : discount factor
            epsilon : exploration rate
        """

        self.ALPHA = alpha
        self.GAMMA = gamma
        self.EPSILON = epsilon
        self.SIZE = 3

        # Initializing current possible actions
        self.possibleActions = self.getPossibleActions()
        self.QStateActionValues = self.InitStateActionValues()
        self.rewards = []


        # super().__init__()
    
    def getPossibleActions(self, state = None):
        """
        returns a list of all possible actions that the agent can take

        (Args)
            state : the hash value of the current game (eg. XOX--X-OX)
        """

        if state:
            # When the tic-tac-toe board is not empty
            return [a for a in self.possibleActions if state[ (a[0] * self.SIZE) + a[1] ] == '-']
        
        else:
            # Empty board: all are possible actions
            return [(j, i) for i in range(0, self.SIZE) for j in range(0, self.SIZE)]
    
    def InitStateActionValues(self):
        """
        Initializes a dictionary containing with empty state action value pairs
        """
        stateActionValues = {}

        for a in self.possibleActions:
            stateActionValues[a] = collections.defaultdict(int)

        return stateActionValues
    
    def getMaxStateAction(self, QStateActions, state):
        """
        returns the action with the highest Q-value

        (Args)
            QStateActions : a copy of the self.QStateActions
            state : the hash value of the current game (eg. XOX--X-OX)
        """

        # Getting all possible actions at current state
        currentPossibleActions = self.getPossibleActions(state)


        # Assigning default values
        maxValue = -99999 #some large negative value
        maxAction = currentPossibleActions[0]

        for action in currentPossibleActions:
            currentValue = QStateActions[action][state]
            if currentValue > maxValue:
                maxValue = currentValue
                maxAction = action

        return maxAction
    
    @abc.abstractmethod
    def selectGreedyAction(self, state):
        pass

    @abc.abstractmethod
    def updateStateActionValues(self, state, action, nextState, reward):
        pass 

# Q-Learning
class QLearner(BaseLearner):
    def __init__(self, size = 3, alpha = 0.5, gamma = 0.9, epsilon = 0.1) -> None:
        """
        Initializes a Q Learning agent
        (Args)
            size : the size of the game (usually 3)
            alpha :  learning rate or step size parameter
            gamma : discount factor
            epsilon : exploration rate
        """

        # Calling base class constructor
        super().__init__(size, alpha, gamma, epsilon)

    def selectGreedyAction(self, state):
        """
        This method will select an action to be performed by the agent

        (Args)
            state : the state representation of the current board (eg. XOX--X-OX)
        """
        # Get action with maximum Q value
        return self.getMaxStateAction(self.QStateActionValues, state)
    
    def updateStateActionValues(self, state, action, nextState, reward):
        """
        updates Q-values for state-action pairs

        (Args)
            state : the hash value of the previous game (eg. XOX--X-OX)
            action : the action perfromed on the previous state
            nextState: the hash value of the current game
            reward: reward for performing the action
        """

        maxValue = 0
        
        if nextState:
            # If nextState is available
            currentPossibleActions = self.getPossibleActions(nextState)
            
            if rd.random() < self.EPSILON:
                nextAction = currentPossibleActions[np.random.choice(len(currentPossibleActions))]
                maxValue = self.QStateActionValues[nextAction][nextState]
            
            else:
                possibleQOptions = [self.QStateActionValues[a][nextState] for a in currentPossibleActions]
                maxValue = max(possibleQOptions)
        
        # Updating the Q-value based on the formula
        self.QStateActionValues[action][state] = \
            self.QStateActionValues[action][state] + \
            self.ALPHA * (reward + self.GAMMA * maxValue - self.QStateActionValues[action][state])

        # Appending the reward of the action
        self.rewards.append(reward)

# SARSA Learning
class SarsaLearner(BaseLearner):
    def __init__(self, size = 3, alpha = 0.5, gamma = 0.9, epsilon = 0.1) -> None:
        """
        Initializes a SARSA Learning agent
        
        (Args)
            size : the size of the game (usually 3)
            alpha :  learning rate or step size parameter
            gamma : discount factor
            epsilon : exploration rate
        """

        # Calling base class constructor
        super().__init__(size, alpha, gamma, epsilon)

    def getEpsilonGreedyAction(self, state):
        """
        returns the action selected by Epsilon-greedy approach

        (Args)
            state : the hash value of the current game (eg. XOX--X-OX)
        """

        # Getting all possible actions at current state
        currentPossibleActions = self.getPossibleActions(state)
        
        # Getting a random number
        randomNumber = np.random.rand()
        maxAction = None
        
        if randomNumber < self.EPSILON:
            # Selcting an action at random
            maxAction = currentPossibleActions[np.random.choice(len(currentPossibleActions))]
        
        else:
            # Getting action with maximum Q-value
            maxAction = self.getMaxStateAction(self.QStateActionValues, state)

        return maxAction
    
    def selectGreedyAction(self, state):
        """
        This method will select an action to be performed by the agent

        (Args)
            state : the state representation of the current board (eg. XOX--X-OX)
        """
        
        # Selects an action using epsilon-greedy approach
        return self.getEpsilonGreedyAction(state)
    
    def updateStateActionValues(self, state, action, nextState, reward):
        """
        updates Q-values for state-action pairs

        (Args)
            state : the hash value of the previous game (eg. XOX--X-OX)
            action : the action perfromed on the previous state
            nextState: the hash value of the current game
            reward: reward for performing the action
        """
        nextActionValue = 0

        if nextState:
            # If there is a possiblity to move to a state

            # Get next action to be performed using epsilon-greedy approach
            nextAction = self.getEpsilonGreedyAction(nextState)
            nextActionValue = self.QStateActionValues[nextAction][nextState]

        else:
            # When the final state has been reached
            nextActionValue = 0

        # Calculating Q value (state-action value)
        self.QStateActionValues[action][state] = \
            self.QStateActionValues[action][state] + \
            self.ALPHA * (reward + self.GAMMA * nextActionValue - self.QStateActionValues[action][state])
        
        self.rewards.append(reward)
