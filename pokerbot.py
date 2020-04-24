import os
import sys

from working_tools import input_file_parser, tree_visualizer
from working_tools.abstraction_generator import abstraction_manager
from working_tools.game_solver.external_sampling import normalize_table
from working_tools.game_solver.solver import solver

if __name__ == '__main__':

    # tree will be the root node of the entire tree
    # parse the file to compute the tree structure
    tree = input_file_parser.parse_tree(os.path.join(os.getcwd(), 'inputs', 'leduc5.txt'))

    # info_sets will contain the complete infostructure of the game
    # parse_infoset reads the file and returns the infostructure
    info_sets = input_file_parser.parse_infoset(os.path.join(os.getcwd(), 'inputs', 'leduc5.txt'), tree)

    # visualize the game tree
    # tree_visualizer.visualize_game_tree(tree, 0)

    # visualize the infostructure of the tree
    # tree_visualizer.visualize_info_structure(tree, info_sets)

    abstraction_set = abstraction_manager.create_abstraction(tree, 2)
    # original = sys.stdout
    # sys.stdout = open('redirect.txt', 'w')
    print('+++ABSTRACTION SET+++')
    # visualization of the new infostructure
    for abstraction_level in abstraction_set:
        # for infoset_list in abstraction_level:
        for infoset in abstraction_level:  # .values():
            print(infoset.name)
            for node in infoset.info_nodes.values():
                print(node.history, end=' ')
            print('')
            print('-----')
            # tree_visualizer.visualize_infoset(tree, infoset, 1)
    # print('++++++++++++++++++++++')
    # sys.stdout = original
    utilities, strategy_table = solver(abstraction_set, 20, 2, tree)
    strategy_table = normalize_table(strategy_table)
    print(utilities)
    print(strategy_table)
