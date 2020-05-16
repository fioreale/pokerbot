import copy

from tree_elements.nature_node import NatureNode
from working_tools.abstraction_generator.tree_navigator import find_tree_height
from working_tools.game_refiner.subgames_calculator import subgame_calculator, compute_probabilities_to_subgame, \
    compress_subgame


def game_strategy_refiner(tree):
    tree_levels = find_tree_height(tree, 0)

    for level in range(tree_levels):

        tree_copy = copy.deepcopy(tree)
        subgames_list = subgame_calculator(tree_copy, level)

        for subgame in subgames_list:

            probabilities_to_subgame = compute_probabilities_to_subgame(subgame)

            compressed_subgame = compress_subgame(subgame)

            new_tree_for_solver = NatureNode()
            new_tree_for_solver = new_tree_for_solver.create_new_tree(subgame, probabilities_to_subgame)

