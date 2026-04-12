# Tic-Tac-Toe RL Project

A Python project that explores how different AI approaches play Tic-Tac-Toe.

This repository implements and compares three algorithms:

- **Q-Learning**
- **SARSA**
- **Min-Max**

## What this project does

The reinforcement learning agents are trained by playing many games and improving over time based on rewards.  
The Min-Max agent does not learn from experience—instead, it calculates the best possible move at each turn.

This makes the project a simple way to study both:

- **Reinforcement learning**
- **Optimal game strategy**

## Project structure

```text
LearningAlgorithms/
DynamicProgramming/
README.md
```

- `LearningAlgorithms/` contains the **Q-Learning** and **SARSA** implementations
- `DynamicProgramming/` contains the **Min-Max** implementation

## Requirements

Install these Python libraries before running the project:

```bash
pip install numpy matplotlib
```

## How to run

### Q-Learning or SARSA

Open the `LearningAlgorithms` folder and run:

```bash
python start.py
```

You will be asked to:

1. Choose an algorithm
2. Enter the number of training episodes

After training, you can play against the agent.  
Performance graphs will be displayed when you finish.

### Min-Max

Open the `DynamicProgramming` folder and run:

```bash
python game.py
```

This starts the Tic-Tac-Toe game using the Min-Max algorithm, which plays optimally.

## Compare Q-Learning and SARSA

To compare both reinforcement learning algorithms, run:

```bash
python algocomparison.py
```

This script compares their performance after training and can also be used to test different hyperparameters.

## Summary

This project shows the difference between:

- **Q-Learning** as an off-policy method
- **SARSA** as an on-policy method
- **Min-Max** as an optimal search-based strategy

It is a useful academic project for understanding how learning-based and rule-based approaches behave in a simple game environment.
