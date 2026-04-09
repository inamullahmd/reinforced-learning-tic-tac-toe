## Starting the Q-learning program

# Importing libraries
from gameplatform import Environment
import matplotlib.pyplot as graph

print("WELCOME TO #TIC-TAC-TOE#")

# creating an environment object by reading number of episodes
gamePlatform = Environment(
    algorithm = input("Choose an algorithm: ql (Q learning) | s (sarsa) : "),
    numberOfEpisodes = int(input("Please enter number of episodes: "))
)

gamePlatform.trainAgent()
gamePlatform.playWithHuman()
gamePlatform.plotWinningsGraph()
gamePlatform.plotDiscountedReward()
gamePlatform.plotConvergenceGraph()