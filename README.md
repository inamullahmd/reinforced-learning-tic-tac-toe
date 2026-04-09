# TicTacToe
This is a academic Reinforced Learning project for Tic Tac Toe game. We'll be implementing three algorithms. Q-Learning, SARSA and Min-Max algorithm. The code is written in Python language.

# Getting started
## Pre-requisites
To execute the code, you need to install the following libraries:
- numpy
- matplotlib
## Executing the code
To implement the Q learning or SARSA, open the folder 'LearningAlgorithms'. Run the following command:
```
LearningAlgorithms> python start.py
```
You'll need to select an algorithm (Q learning/ SARSA) and enter the number of episodes. The agent will be trained for the given # of episodes. After the training is done, you can play against the agent as many times you want. 

After you're done with playing, then some performance graphs will be displayed.

To implement the Dynamic Programming, open the folder "DynamicProgramming", then run the following command:
```
DynamicProgramming> python game.py
```

When you run this, the tic tac toe game will be started. You can play as many times as you want. Using Min-max algorithm, the best optimal move is calculated. You'll find very challenging to defeat the computer agent.

## Comparing the Q learning and SARSA
IF you want to compare the performances of  both these algorithms, you can execute the following command:
```
LearningAlgorithms> python algocomparison.py
```
This command will compare the Q learning and SARSA algorithms after their training of about 100000 episodes. This code also has a variations of these algorithms compared such as changing learning rate etc.,

You can call the function on your own, if you want to vary other parameters such as discount factor and exploration rate.