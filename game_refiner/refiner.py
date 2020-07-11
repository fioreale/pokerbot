import copy

from game_model.nature_node import NatureNode
from game_abstraction.tree_navigator import find_tree_height
from game_refiner.subgames_calculator import subgame_calculator, compute_probabilities_to_subgame, \
    compress_subgame, normalize_probabilities_to_subgame
from game_solver.external_sampling import normalize_table
from game_solver.solver import solver


def game_strategy_refiner(tree, time_steps):
    tree_levels = find_tree_height(tree, 0)

    for level in range(tree_levels):
        tree_copy = copy.deepcopy(tree)
        tree_copy.update_infosets_after_deep_copy(tree_copy)
        subgames_list = subgame_calculator(tree_copy, level)
        index = 1
        list_lenght = len(subgames_list)
        for subgame in subgames_list:
            print('\nGame refiner, tree level: ' + str(level)
                  + ', subgame: '
                  + str(index)
                  + '/' + str(list_lenght))
            index += 1
            probabilities_to_subgame = compute_probabilities_to_subgame(subgame)
            probabilities_to_subgame = normalize_probabilities_to_subgame(probabilities_to_subgame)

            compress_subgame(subgame)
            new_tree_for_solver = NatureNode()
            new_tree_for_solver = new_tree_for_solver.create_new_tree(subgame, probabilities_to_subgame)
            abstraction_set = new_tree_for_solver.get_infosets_of_tree()
            utilities, strategy_table = solver(abstraction_set, time_steps, 2, new_tree_for_solver)
            strategy_table = normalize_table(strategy_table)
            remap_strategies_to_tree(strategy_table, new_tree_for_solver, tree)


def remap_strategies_to_tree(strategy_table, new_tree_for_solver, tree):
    for child in new_tree_for_solver.children.values():
        strategies_to_remap = strategy_table[child.infoset.name]
        original_node = tree.node_finder(child.history)
        original_node.strategies_probabilities = []
        for action in original_node.actions:
            original_node.strategies_probabilities.append(strategies_to_remap[action])
