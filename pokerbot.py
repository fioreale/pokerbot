import copy
import os
import logging

from working_tools import input_file_parser
from working_tools.abstraction_generator import abstraction_manager
from working_tools.game_refiner.subgames_calculator import subgame_calculator
from working_tools.game_solver.external_sampling import normalize_table
from working_tools.game_solver.solver import solver
from working_tools.game_refiner.strategies_mapper import apply_strategies_to_nodes

FILE_NAME = 'leduc5.txt'

if __name__ == '__main__':

    logging.basicConfig()

    pokerbot_logger = logging.getLogger('pokerbot')
    pokerbot_logger.setLevel(logging.WARNING)

    # tree will be the root node of the entire tree
    # parse the file to compute the tree structure
    tree = input_file_parser.parse_tree(os.path.join(os.getcwd(), 'text_files', 'inputs', FILE_NAME))

    # info_sets will contain the complete infostructure of the game
    # parse_infoset reads the file and returns the infostructure
    info_sets = input_file_parser.parse_infoset(os.path.join(os.getcwd(), 'text_files', 'inputs', FILE_NAME), tree)

    # parse again
    # compressed_tree = input_file_parser.parse_tree(os.path.join(os.getcwd(), 'text_files', 'inputs', FILE_NAME))

    # compressed_infosets = input_file_parser.parse_infoset(os.path.join(os.getcwd(), 'text_files', 'inputs', FILE_NAME),
    #                                                       compressed_tree)

    # visualize the game tree
    # original = sys.stdout
    # sys.stdout = open('tree.txt', 'w')
    # tree_visualizer.visualize_game_tree(tree, 0)
    # sys.stdout = original
    # visualize the infostructure of the tree
    # tree_visualizer.visualize_info_structure(tree, info_sets)

    abstraction_set = abstraction_manager.create_abstraction(tree, '1')
    abstraction_set.extend(abstraction_manager.create_abstraction(tree, '2'))
    # tree_visualizer.visualize_game_tree(compressed_tree, 0)

    print('INITIAL NUMBER OF INFOSETS:', end=' ')
    print(info_sets.get_number_of_infosets())
    print('FINAL NUMBER OF INFOSETS:', end=' ')
    print(len(abstraction_set))
    # original = sys.stdout
    # sys.stdout = open('redirect.txt', 'w')
    print('+++ABSTRACTION SET+++')
    # visualization of the new infostructure
    for infoset in abstraction_set:
        # for infoset_list in abstraction_level:
        print(infoset.name)
        # for node in infoset.info_nodes.values():
        #     print(node.history, end=' ')
        print('-----')
    print('++++++++++++++++++++++')
    # sys.stdout = original

    utilities, strategy_table = solver(abstraction_set, 1000, 2, tree)
    strategy_table = normalize_table(strategy_table)
    print(utilities)
    print(strategy_table)

    apply_strategies_to_nodes(abstraction_set, strategy_table)

    subgames = subgame_calculator(tree, 4)

    print('hello world')
