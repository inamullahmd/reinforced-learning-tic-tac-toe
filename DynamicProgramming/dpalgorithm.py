## Min Max Algorithm for Dynamic Programming

# Importing libraries
import math

# MinMax Algorithm
class Algorithm:
    def __init__(self, playerChar, systemChar) -> None:
        """
        Initializes a MinMax class with Board and Game objects
        """
        self.playerChar = playerChar
        self.systemChar = systemChar
        self.moves = {}
    
    def minimax(self, board, depth:int, doMax:bool):
        """
        Min Max algorithm to calculate the max/min score possible
        
        (Args)
            board: the current Board object
            depth: to denote the depth of the recursive function
            doMax: when True, algorithm considers max scores else min scores
        """

        # Checking if the game is over
        winner = board.gameWinner()

        if winner == '-':
            return 0
        
        elif winner == self.playerChar:
            return -10
        
        elif winner == self.systemChar:
            return 10
        if doMax:
            bestScore = - math.inf
            
            for move in board.getEmptyCells():
                board.fillACell(move, self.systemChar)
                score = self.minimax(board, depth + 1, False)
                board.undo()
                bestScore = max(score, bestScore)
            
            return bestScore

        else:
            bestScore = math.inf
            
            for move in board.getEmptyCells():
                board.fillACell(move, self.playerChar)
                score = self.minimax(board, depth + 1, True)
                board.undo()
                bestScore = min(score, bestScore)
            
            return bestScore

    def bestMove(self, board):
        bestScore = - math.inf
        bestMove = None
        moves = {}
        
        for move in board.getEmptyCells():
            board.fillACell(move, self.systemChar)
            score = self.minimax(board, 0, False)
            if len(board.getEmptyCells()) >= 5:
                moves[move[0]*3 + move[1] + 1] = score
            board.undo()
            if (score > bestScore):
                bestScore = score
                bestMove = move

        return bestMove