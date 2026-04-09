## Board class and its respective methods

# Importing Libraries
import numpy as np
from dpalgorithm import Algorithm
# Board Class
class Board:
    def __init__(self, length = 3) -> None:
        """
        Initializes a nXn matrix of given length (default 3)
        """

        self.length = length
        self.board = np.full((length, length), '-')
        self.movesHistory = []
    
    def undo(self):
        """
        On revoking, undoes the last move
        """
        if self.movesHistory:
            lastMove = self.movesHistory.pop()
            for (index, char) in enumerate(lastMove):
                self.board[self.extractCellPosition(index)] = char

    def stateRepr(self):
        """
        returns a string with the board values
        
        (Args)
            isNumeric: when True, returns string 1s and 0s else in Xs and Os
        """

        repr = ""
        for row in self.board:
            for value in row:
                repr += str(value)
        
        return repr

    def fillACell(self, position:tuple, char):
        """
        places a 'char' at given position

        (Args)
            position: a tuple with row no and column no
            char: X or O
        """

        self.movesHistory.append(self.stateRepr())
        self.board[position] = char

    def extractCellPosition(self, index:int):
        """
        Given a position in a one dimensional array,
        calculates the row and column in a two dimensional array
        """

        return (index // self.length, index % self.length)

    def display(self):
        """
        displays the current board
        """
        print("\033[91mTIC TAC TOE GAME\033[92m")
        for i in range(self.length):
            print("-" + "----" * self.length)
            x = "| "
            for j in range(self.length):
                x += self.board[i,j] + " | "
            print(x)
        print("-" + "----" * self.length, end="\033[0m\n")

    def isGameTied(self):
        """
        returns True if the game is tied
        """
        
        if (np.char.count(self.board, '-').sum() == 0):
            return True

        return False

    def gameWinner(self):
        """
        returns game winner (X|O), '-' if draw, False if result not available
        """

        # checking if the game is draw
        if self.isGameTied():
            return '-'

        # Checking row/column wise
        for i in range(0,self.length):
            # Checking row wise for same value
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                if self.board[i][0] != '-':
                    return self.board[i][0]

            # Checking column wise for same value
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                if self.board[0][i] != '-':
                    return self.board[0][i] 
        
        # Checking diagonal-wise
        # diagonal 1
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[1][1] != '-':
                return self.board[1][1]
        
        # diagonal 2
        if self.board[2][0] == self.board[1][1] == self.board[0][2]:
            if self.board[1][1] != '-':
                return self.board[1][1]
        
        return False

    def getEmptyCells(self):
        """
        Returns list of tuples with row and column number
        of cells which are empty (i.e., = '-')
        """

        positions = []

        for i in range(0, self.length):
            for j in range(0, self.length):
                if self.board[i, j] == '-':
                    positions.append((i, j))
        
        return positions

# Game class
class Game:
    def __init__(self, length = 3) -> None:
        """
        Initializes the tic tac toe game
        """
        self.length = length
        self.board = Board(length)
        self.playerChar = '-'
        self.systemChar = '-'
        self.currentPlayer = '-'
        self.end = False
        self.algo = None
        
        # Creating mapping between numeric cell values and row & column values
        self.mapper = {}
        for i in range(0, self.length):
            for j in range(0, self.length):
                # tuple : numeric cell value
                self.mapper[(i, j)] = (i * 3) + j + 1
                
                # numeric cell value : tuple
                self.mapper[(i * 3) + j + 1] = (i, j)
    
    def readFromUser(self):
        """
        method to read initial input from the user
        """
        turn = input("Do you want to play first (Y/N)? ")

        if turn.upper() == 'Y':
            # If user wants to play first
            self.playerChar = 'X'
            self.systemChar = 'O'
            self.currentPlayer = 'H'
        
        elif turn.upper() == 'N':
            # If user asks system to play first
            self.playerChar = 'O'
            self.systemChar = 'X'
            self.currentPlayer = 'S'
        
        self.algo = Algorithm(self.playerChar, self.systemChar)
        
    def displayFixedPositions(self):
        """
        Display fixed numeric positions of the game board
        """

        print("\033[94mFixed positions:")
        
        for i in range(3):
            print("-" + "----" * 3)
            x = "| "
            
            for j in range(3):
                x += str(3 * i + j + 1) + " | "
            
            print(x)
        
        print("-" + "----" * 3, end="\033[0m\n")

    def readNextMove(self):
        """
        reads next move from the user
        """

        validPositions = []

        for (i,j) in self.board.getEmptyCells():
            validPositions.append(self.mapper[(i, j)])
        
        print("Available positions: ", validPositions)

        # reading move from the user
        validInput = False
        move = None
        while not validInput:
            move = int(input("your move: "))
            if move not in validPositions:
                print("Invalid position")
            else:
                validInput = True
        
        return self.mapper[move]

    def startGame(self):
        """
        method to start the game by reading input from the user
        """

        # reading initial input from the user
        self.readFromUser()

        # displaying the fixed cell position values
        self.displayFixedPositions()
        step = 0

        while not self.end:
            if self.currentPlayer == 'H':
                # reading user's move
                self.board.fillACell(self.readNextMove(), self.playerChar)
                self.board.display()
                self.currentPlayer = 'S'
            
            elif self.currentPlayer == 'S':
                # performing system's best move
                self.board.fillACell(self.algo.bestMove(self.board), self.systemChar)
                self.board.display()
                self.currentPlayer = 'H'

            if self.board.gameWinner():
                # If the game ended in a result, ending game
                self.displayWinner(self.board.gameWinner())
                self.end = True
            
            step += 1

            if self.end:
                if(input("Do you want to play again (Y/N)? ").upper() == 'Y'):
                    self.board = Board(3)
                    self.end = False
                    self.startGame()
                else:
                    break

    def displayWinner(self, winner):

        if winner == self.playerChar:
            print("\033[1m\033[32mCongrats! You won. Well played", end="\033[0m\n")

        elif winner == self.systemChar:
            print("\033[1m\033[32mYAY! I won. Better luck next time.", end="\033[0m\n")
        
        elif winner == '-':
            print("\033[1m\033[32mIt's a DRAW! Tough game!!", end="\033[0m\n")

game = Game(3)
game.startGame()
# game.algo.plot()