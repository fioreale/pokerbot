import os
import logging

from game_builder import input_file_parser
from game_abstraction import abstraction_manager
from game_abstraction.tree_navigator import file_strategies_saver, json_regrets_saver
from game_builder.tree_visualizer import visualize_regrets
from game_refiner.refiner import game_strategy_refiner
from game_solver.external_sampling import normalize_table
from game_solver.solver import solver
from game_refiner.strategies_mapper import apply_strategies_to_nodes
import sys
from pathlib import Path
from datetime import datetime
from constants import FILE_NAME, SOLVER_TIME_STEPS, REFINER_TIME_STEPS, COMPRESS_PLAYER_2, ABSTRACTION_PERCENTAGE, \
    WIZARD_COEFFICIENT, PERFORM_ABSTRACTION, PERFORM_REFINEMENT, PRINT_BOTH_STRATEGIES, SAVE_REGRETS_TO_JSON, \
    SAVE_STRATEGY_TO_FILE, VISUALIZE_PLOT

if __name__ == '__main__':

    logging.basicConfig()

    pokerbot_logger = logging.getLogger('pokerbot')
    pokerbot_logger.setLevel(logging.WARNING)

    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d__%H_%M_%S")
    percentage_array = [(0.55, 1.25), (0.7700000000000002, 2.5), (0.8600000000000003, 4.0), (0.8800000000000003, 4.75)]

    # tree will be the root node of the entire tree
    # parse the file to compute the tree structure
    tree = input_file_parser.parse_tree(os.path.join(os.getcwd(), 'text_files', 'inputs', FILE_NAME))

    # info_sets will contain the complete infostructure of the game
    # parse_infoset reads the file and returns the infostructure
    info_sets = input_file_parser.parse_infoset(os.path.join(os.getcwd(), 'text_files', 'inputs', FILE_NAME),
                                                tree)

    total_number_of_infosets = len(info_sets.info_sets2) + len(info_sets.info_sets1)

    if PERFORM_ABSTRACTION:
        if COMPRESS_PLAYER_2:
            abstraction_set = abstraction_manager.create_abstraction(tree, '1', total_number_of_infosets,
                                                                     ABSTRACTION_PERCENTAGE, WIZARD_COEFFICIENT)
            abstraction_set.extend(
                abstraction_manager.create_abstraction(tree, '2', total_number_of_infosets, ABSTRACTION_PERCENTAGE,
                                                       WIZARD_COEFFICIENT))
        else:
            abstraction_set = abstraction_manager.create_abstraction(tree, '1', total_number_of_infosets,
                                                                     ABSTRACTION_PERCENTAGE, WIZARD_COEFFICIENT)
            abstraction_percentage = len(abstraction_set) / len(info_sets.info_sets1)
            abstraction_set.extend(info_sets.info_sets2)
            print('PERC: ' + str(ABSTRACTION_PERCENTAGE) + ' COEFF: ' + str(WIZARD_COEFFICIENT) + ' compression '
                                                                                                  'percentage: ' +
                  str(abstraction_percentage))
            Path("text_files/outputs").mkdir(parents=True, exist_ok=True)
            original = sys.stdout
            sys.stdout = open('text_files/outputs/percentages_' + current_time + '.txt', 'a')
            print('PERC: ' + str(ABSTRACTION_PERCENTAGE) + ' COEFF: ' + str(WIZARD_COEFFICIENT) + ' compression '
                                                                                                  'percentage: ' +
                  str(abstraction_percentage))
            sys.stdout = original
    else:
        abstraction_set = info_sets.info_sets1
        abstraction_set.extend(info_sets.info_sets2)

    regrets_history, strategy_table = solver(abstraction_set, SOLVER_TIME_STEPS, 2, tree)

    print(regrets_history)

    if SAVE_REGRETS_TO_JSON:
        json_regrets_saver(regrets_history)

    if VISUALIZE_PLOT:
        visualize_regrets(regrets_history)

    strategy_table = normalize_table(strategy_table)
    apply_strategies_to_nodes(abstraction_set, strategy_table)

    if PERFORM_REFINEMENT:
        game_strategy_refiner(tree, REFINER_TIME_STEPS)

    if SAVE_STRATEGY_TO_FILE:
        # save strategies to file
        game_name = FILE_NAME
        abstraction_boolean = 'yes_abstraction' if PERFORM_ABSTRACTION else 'no_abstraction'
        refinement_boolean = 'yes_refinement' if PERFORM_REFINEMENT else 'no_refinement'
        file_name = game_name[:-4] + '_' + abstraction_boolean + '_' + refinement_boolean
        file_strategies_saver(tree, file_name, PRINT_BOTH_STRATEGIES)
