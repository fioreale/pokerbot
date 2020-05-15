import copy

from working_tools.abstraction_generator.tree_navigator import find_tree_height
from working_tools.game_refiner.subgames_calculator import subgame_calculator, compute_probabilities_to_subgame


def game_strategy_refiner(tree):
    tree_levels = find_tree_height(tree, 0)

    for level in range(tree_levels):

        subgames_list = subgame_calculator(tree, level)

        for subgame in subgames_list:

            probabilities_to_subgame = compute_probabilities_to_subgame(subgame)

            subgame_copy = copy.deepcopy(subgame)

            compressed_subgame = compress_subgame(subgame_copy, probabilities_to_subgame)
