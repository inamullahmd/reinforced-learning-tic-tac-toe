## PLATFORM FOR TERMINAL BASED GUI

# Importing libraries
from game import TicTacToe
from algocollections import QLearner, SarsaLearner
from matplotlib import pyplot as graph
from tqdm import tqdm

class Environment:

    def __init__(self, algorithm:str, numberOfEpisodes, alpha = 0.1, gamma = 0.9, epsilon = 0.1) -> None:
        """
        Initializes an environment to train and play
        Tic-Tac-Toe with Q-learning

        (Args)
            algorithn: ql for Q learning | s for SARSA Learning
            numberOfEpisodes : Total number of games to be used to train the agent
            alpha (default 0.5) :  learning rate or step size parameter
            gamma (default 0.9): discount factor
            epsilon (default 0.1): exploration rate
        """

        self.numberOfEpisodes = numberOfEpisodes
        self.qValues = []
        self.rewards = []

        if algorithm:
            if algorithm.lower() == 'ql':
                self.agent = QLearner(
                    alpha = alpha,
                    gamma = gamma,
                    epsilon = epsilon
                )
                self.algoName = "Q-Learning"
            elif algorithm.lower() == 's':
                self.agent = SarsaLearner(
                    alpha = alpha,
                    gamma = gamma,
                    epsilon = epsilon
                )
                self.algoName = "SARSA Learning"
            else:
                raise Exception("Invalid value")
        else:
            raise Exception("Invalid value")

    def playWithHuman(self):
        """
        Playing an human against the trained agent
        """

        while True:
            # Initializing a game with the trained agent
            ticTacToeGame = TicTacToe(self.agent)
            ticTacToeGame.startGame()

            # Game completed, reading from user
            # whether user wants to play again
            if(input("Would you like to play again(Y/N)? ") != "Y"):
                break

            print("Let's play again!!")

    def trainAgent(self):
        """
        trains the Q-learning agent for given number of episodes
        """

        for i in tqdm(range(1, self.numberOfEpisodes + 1), desc = "training agent ", ):

            # Creating a local object of the game
            ticTacToeGame = TicTacToe(self.agent)

            # Starting training of the agent
            ticTacToeGame.startGame(training = True)

            # Appending the state action values
            self.qValues.append(self.agent.QStateActionValues[(0,0)]['----X----'])
            
            # Appending the reward
            self.rewards.append(ticTacToeGame.reward)
            
    def plotWinningsGraph(self):
        """
        plots a graphing with
            Win %
            Loss %
            Draw %
        with respect to number of episodes
        """
        gameDrawPercentages = []
        gameWinPercentages = []
        gameLossPercentages = []
        gameDrawCount = gameWinCount = gameLossCount = 0

        index = 0
        # counting counts based on reward values
        # reward = 0 (Draw) | 1 (Win) | -1 (Loss)
        for reward in self.rewards:
            if reward == 0:
                gameDrawCount += 1
            elif reward == 1:
                gameWinCount += 1
            elif reward == -1:
                gameLossCount += 1
            
            index += 1
            
            # Calculating individual percentages and appending to a list
            gameDrawPercentages.append(gameDrawCount * 100 / index)
            gameWinPercentages.append(gameWinCount * 100 / index)
            gameLossPercentages.append(gameLossCount * 100 / index)
        
        totalPercentage = 100 / (index + 1)
        print("Q-LEARNING AGENT STATS")

        print("WIN % ", str(round(gameWinCount * totalPercentage, 2)))
        print("LOSS % ", str(round(gameLossCount * totalPercentage, 2)))
        print("DRAW % ", str(round(gameDrawCount * totalPercentage, 2)))

        graph.plot( gameDrawPercentages, label = "DRAW %")
        graph.plot( gameWinPercentages, label = "WIN %")
        graph.plot( gameLossPercentages, label = "LOSS %")

        graph.xlabel("Number of episodes")
        graph.ylabel("percentages")
        graph.title("Q Learning - Number of episodes Vs Percentages")
        graph.legend()
        graph.show()

    def plotDiscountedReward(self):
        """
        plots a graph with cumulative reward w.r.t number of episodes
        """
        cumReward = []
        cumSum = 0

        # for loop to calculate the cumulative sum of rewards
        for i in range(0, len(self.rewards)):
            cumSum = cumSum + (self.rewards[i]/(i+1))
            cumReward.append(cumSum)
        
        graph.plot(cumReward)
        graph.title('Discounted cumulative reward vs. Episodes')
        graph.ylabel('Discounted cumulative reward')
        graph.xlabel('Episodes')
        graph.show()

    def plotConvergenceGraph(self):
        graph.plot(self.qValues)
        graph.title('# episodes vs. Q Values')
        graph.ylabel('Q Values')
        graph.xlabel('Episodes')
        graph.show()