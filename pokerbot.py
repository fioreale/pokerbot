import os
import logging

from working_tools import input_file_parser
from working_tools.abstraction_generator import abstraction_manager
from working_tools.abstraction_generator.tree_navigator import file_strategies_saver
from working_tools.game_refiner.refiner import game_strategy_refiner
from working_tools.game_simulator import game_simulator
from working_tools.game_solver.external_sampling import normalize_table
from working_tools.game_solver.solver import solver
from working_tools.game_refiner.strategies_mapper import apply_strategies_to_nodes
import matplotlib.pyplot as plt
import numpy as np
from constants import FILE_NAME, SOLVER_TIME_STEPS, REFINER_TIME_STEPS

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

    abstraction_set = abstraction_manager.create_abstraction(tree, '1')
    abstraction_set.extend(abstraction_manager.create_abstraction(tree, '2'))

    regrets_history, strategy_table = solver(abstraction_set, SOLVER_TIME_STEPS, 2, tree)

    print(regrets_history)

    plt.figure()
    plt.plot(np.array(regrets_history), 'r')
    plt.show()

    strategy_table = normalize_table(strategy_table)
    apply_strategies_to_nodes(abstraction_set, strategy_table)

    game_strategy_refiner(tree, REFINER_TIME_STEPS)

    # save strategies to file
    file_strategies_saver(tree)

    simulation_results = game_simulator.play_games(tree, 1000)
    print('')
    print('------------------------------------')
    print('Player 1 expected return = ', end='')
    print('{0:+f}'.format(simulation_results))
    print('Player 2 expected return = ', end='')
    print('{0:+f}'.format(-simulation_results))
    print('------------------------------------')
