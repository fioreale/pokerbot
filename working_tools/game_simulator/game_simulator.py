import numpy as np


def play_games(tree, n_games):
    results = []
    for t in range(n_games):
        results.append(tree.play())
    average_results = np.mean(results)
    return average_results
