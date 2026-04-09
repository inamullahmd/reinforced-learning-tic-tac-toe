## TIC TAC TOE GAME ##

# Importing Libraries
import random as rd
from algocollections import BaseLearner
import numpy as np

class TicTacToe:

    def __init__(self, agent: BaseLearner) -> None:
        """
        Initializes a Tic-Tac-Toe game with a Q-learning agent

        (Args)
            agent : A Q-learning class object
        """

        self.agent = agent
        self.agentChar = 'O' # uses this character for agents moves
        self.playerChar = 'X' # uses this character for players moves

        # Initializes an empty board 
        self.board = np.full((3, 3), '-')
    
    def updateMove(self, move: tuple, character: str):
        """
            Updates the board at given position with given character

            (Args)
                move : The position with row and column index number as tuple
                character : The character(X|O) to be updated with 
        """

        self.board[move[0]][move[1]] = character
    
    def displayGame(self):
        """
        Displays the board in a custom formatted manner
        """

        print("========================")
        print("X - TIC TAC TOE GAME - O")
        print("========================")
        
        for i in range(3):
            print("-" + "----" * 3)
            xb = "| "
            for j in range(3):
                xb += str(self.board[i][j]) + " | "
            print(xb)
        print("-" + "----" * 3)

    def getResult(self):
        """
        returns
            [1] if agent wins
            [-1] if player wins
            [0] if game ends in draw
            False if inconclusive
        """

        # Checking row/column wise
        for i in range(0,3):
            # Checking row wise for same value
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                if self.board[i][0] != '-':
                    return 1 if self.board[i][0] == self.agentChar else -1

            # Checking column wise for same value
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                if self.board[0][i] != '-':
                    return 1 if self.board[0][i] == self.agentChar else -1  
        
        # Checking diagonal-wise
        # diagonal 1
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[1][1] != '-':
                return 1 if self.board[1][1] == self.agentChar else -1 
        
        # diagonal 2
        if self.board[2][0] == self.board[1][1] == self.board[0][2]:
            if self.board[1][1] != '-':
                return 1 if self.board[1][1] == self.agentChar else -1 
        
        return False

    def isBoardAllFilled(self):
        """
        helper function to check whether the entire board is filled
        """

        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        
        return True
    
    def isGameTied(self):
        """
        checks whether the current game is tied
        """

        if self.isBoardAllFilled():
            if not self.getResult():
                return True
            
        return False
    
    def generateHashBoard(self):
        """
        returns a string representation of the current board
        """

        positions = ''
        for row in self.board:
            for item in row:
                positions += item
        
        return positions

    def getNewStateAction(self, previousState, previousAction):
        """
        generates the next move for the agent
        """

        # generating hash repr. of current board
        newState = self.generateHashBoard()

        # generating next action using greedy action
        newAction = self.agent.selectGreedyAction(newState)

        # Updating the state-action values
        self.agent.updateStateActionValues(previousState, previousAction, newState, 0)

        return newState, newAction

    def placeAtRandom(self):
        """
        Performing a random move to train the agent
        """

        possibilities = []
        
        # Getting all empty cells on the board
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    possibilities.append((i,j))
        
        # selecting a random action
        action = possibilities[rd.randint(0, len(possibilities) - 1)]

        # Updating the action
        self.board[action[0]][action[1]] = self.playerChar

    def trainAgent(self):
        """
        method to train the Q-learning agent
        """

        # Performing a random move
        if rd.random() < 0.5: 
            self.placeAtRandom()
        
        currentAction = None
        while True:
            if not currentAction:
                # generating hash repr. of current board
                state = self.generateHashBoard()

                # generating next action using greedy action
                currentAction = self.agent.selectGreedyAction(state)
            
            # update the agents move
            self.updateMove(currentAction, self.agentChar)

            # Getting current game result
            gameResult = self.getResult()
            if gameResult:
                self.reward = gameResult
                break
            if self.isGameTied():
                self.reward = 0
                break
            
            # Making a random move against the agent
            self.placeAtRandom()

            # Getting current game result
            gameResult = self.getResult()
            if gameResult:
                self.reward = gameResult
                break
            if self.isGameTied():
                self.reward = 0
                break
            
            # Getting next state and action
            state, currentAction = self.getNewStateAction(state, currentAction)
        
        # Update the state action values
        self.agent.updateStateActionValues(state, currentAction, None, self.reward)
    
    def displayPositions(self):
        """
        displays the cell numbers corresponding to (1-9)
        """

        print("Fixed Positions: ")
        for i in range(3):
            print("-" + "----" * 3)
            x = "| "
            for j in range(3):
                x += str(3 * i + j + 1) + " | "
            print(x)
        
        print("-" + "----" * 3)

    def readHumanMove(self):
        """
        Reading the next move from the player
        """

        while True:
            position = int(input("select a position(1-9): "))

            # Checking if valid board cell number
            if position not in range(1, 10):
                print("Invalid position")
            
            # Checking if the cell is empty
            elif self.board[(position - 1) // 3][(position - 1) % 3] != '-':
                print("Invalid position")
            
            # If it's valid and empty then make the move
            else:
                self.board[(position - 1) // 3][(position - 1) % 3] = self.playerChar
                break
    
    def playWithHuman(self):
        """
        method to play a game between agent and player
        """

        # display fixed positions (1-9)
        self.displayPositions()

        # Check whether the user wants to go first
        playFirst = input("Do you want to play first (Y/N)? ")
        
        if playFirst.upper() == 'Y':
            # read human move
            self.readHumanMove()
        
        elif playFirst.upper() != 'N':
            # Invalid option, so read again
            print("Invalid option")
            self.playWithHuman()

        currentAction = None
        
        while True:
            if not currentAction:
                # generating hash repr. of current board
                state = self.generateHashBoard()
                
                # generating next action using greedy action
                currentAction = self.agent.selectGreedyAction(state)
            
            # Update the agents move
            self.updateMove(currentAction, self.agentChar)
            
            # Get result of the game and add the reward
            if self.getResult():
                reward = self.getResult()
                break
            if self.isGameTied():
                reward = 0
                break
            
            # display the game on terminal
            self.displayGame()
            print("Available positions to choose")
            hashboard = self.generateHashBoard()
            
            availablePositions = [j+1 for j,i in enumerate(hashboard) if i=='-']  
            print(availablePositions)
            
            self.readHumanMove()
            
            if self.getResult():
                reward = self.getResult()
                break
            if self.isGameTied():
                reward = 0
                break
            
            # Get next action and state
            state, currentAction = self.getNewStateAction(state, currentAction)

            self.displayGame()
        
        self.displayGame()
        
        # Display the result
        if reward == 0:
            print("It was a draw!")
        elif reward == -1:
            print("You won!")
        else:
            print("You lost!")

        # when final state is reached
        self.agent.updateStateActionValues(state, currentAction, None, reward)

    def startGame(self, training = False):
        """
        starts the game with training or with player
        
        (Args)
            training : 
                True : starts training the agent
                False : starts the game with human
        """
        if training:
            self.trainAgent()
        else:
            self.playWithHuman()
