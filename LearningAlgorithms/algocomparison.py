from gameplatform import Environment
from matplotlib import pyplot as graph

def avgCalculator(rewards):
    totals = []
    for i in range(len(rewards)):
        totals.append(sum(rewards[:i+1])/(i+1))

    return totals

def compareAlgorithms(episodes):

    # Creating Q-learning agent
    envQ = Environment(algorithm = 'ql', numberOfEpisodes = episodes, alpha = 0.1)

    # Creating sarsa learning agent
    envS = Environment(algorithm = 's', numberOfEpisodes = episodes, alpha = 0.1)

    envQ.trainAgent()
    envS.trainAgent()
    
    # if type == 'rewards':
    graph.plot(avgCalculator(envQ.rewards), label = "Q-Learning")
    graph.plot(avgCalculator(envS.rewards), label = "SARSA")
    graph.title("Average reward over " + str(episodes) + " episodes")
    graph.xlabel("# episodes")
    graph.ylabel("Average reward")
    graph.legend()
    graph.show()
    
    # elif type == 'wins':
    graph.plot(envQ.qValues, label = "Q-Learning")
    graph.plot(envS.qValues, label = "SARSA")
    graph.title("Q values over " + str(episodes) + " episodes")
    graph.xlabel("# episodes")
    graph.ylabel("Q Values")
    graph.legend()
    graph.show()

def multiHyperParameters(algorithm, episodes, alpha = None, gamma = None, epsilon = None):
    """
    performing q-learning with different alpha values
    """

    if alpha:
        for val in alpha:
            print("Training agent with alpha ", val)
            env = Environment(algorithm, episodes, alpha = val)
            env.trainAgent()
            graph.plot(avgCalculator(env.rewards), label = env.algoName+ " with alpha = " + str(val))
    
    elif gamma:
        for val in gamma:
            print("Training agent with gamma ", val)
            env = Environment(algorithm, episodes, gamma = val)
            env.trainAgent()
            graph.plot(avgCalculator(env.rewards), label = env.algoName+ " with gamma = " + str(val))
    
    elif epsilon:
        for val in epsilon:
            print("Training agent with epsilon ", val)
            env = Environment(algorithm, episodes, epsilon = val)
            env.trainAgent()
            graph.plot(avgCalculator(env.rewards), label = env.algoName+ " with epsilon = " + str(val))

    
    graph.title("Average reward over " + str(episodes) + " episodes")
    graph.xlabel("# episodes")
    graph.ylabel("Average reward")
    graph.legend()
    graph.show()

compareAlgorithms(100000)
# multiHyperParameters('ql', 100000, alpha = [0.1, 0.3, 0.5, 0.7, 0.9])
# multiHyperParameters('s', 100000, alpha = [0.1, 0.3, 0.5, 0.7, 0.9])