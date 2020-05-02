import os
import logging
from working_tools import input_file_parser, tree_visualizer
from working_tools.abstraction_generator import abstraction_manager

FILE_NAME = 'leduc5.txt'

if __name__ == '__main__':

    logging.basicConfig()

    pokerbot_logger = logging.getLogger('pokerbot')
    pokerbot_logger.setLevel(logging.WARNING)

    # tree will be the root node of the entire tree
    # parse the file to compute the tree structure
    tree = input_file_parser.parse_tree(os.path.join(os.getcwd(), 'inputs', FILE_NAME))

    # info_sets will contain the complete infostructure of the game
    # parse_infoset reads the file and returns the infostructure
    info_sets = input_file_parser.parse_infoset(os.path.join(os.getcwd(), 'inputs', FILE_NAME), tree)

    # parse again
    compressed_tree = input_file_parser.parse_tree(os.path.join(os.getcwd(), 'inputs', FILE_NAME))

    compressed_infosets = input_file_parser.parse_infoset(os.path.join(os.getcwd(), 'inputs', FILE_NAME),
                                                          compressed_tree)

    # visualize the game tree
    # tree_visualizer.visualize_game_tree(tree, 0)

    # visualize the infostructure of the tree
    # tree_visualizer.visualize_info_structure(tree, info_sets)

    compressed_tree = abstraction_manager.create_abstraction(tree, compressed_tree, 2)
    # tree_visualizer.visualize_game_tree(compressed_tree, 0)

    # original = sys.stdout
    # sys.stdout = open('redirect.txt', 'w')
    # print('+++ABSTRACTION SET+++')
    # visualization of the new infostructure
    # for abstraction_level in abstraction_set:
    #     # for infoset_list in abstraction_level:
    #     for infoset in abstraction_level:  # .values():
    #         print(infoset.name)
    #         for node in infoset.info_nodes.values():
    #             print(node.history, end=' ')
    #         print('')
    #         print('-----')
    #         # tree_visualizer.visualize_infoset(tree, infoset, 1)
    # print('++++++++++++++++++++++')
    # # sys.stdout = original
    # utilities, strategy_table = solver(abstraction_set, 20, 2, tree)
    # strategy_table = normalize_table(strategy_table)
    # print(utilities)
    # print(strategy_table)
