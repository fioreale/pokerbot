from game_abstraction.tree_navigator import json_regrets_reader
from game_model.terminal_node import TerminalNode
from matplotlib import pyplot as plt
import numpy as np

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'


class bcolors:
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''


def in_chars(name):
    # printing a string as a list of characters
    return [char for char in name]


def visualize_game_tree(el, level):
    # for each node passed to the recursive function is considered the dictionary of the relative children
    if el.children is not None:
        for key, value in el.children.items():
            # printing in a depth-first search fashion
            # on a single line is highlighted a path going down level by level
            print('{:<15}'.format(value.history[-1] + '  ->'), end='')
            # called the function for the subsequent level, starting from the current node
            visualize_game_tree(value, level + 1)
            player = 1
            # check for the payoffs print, done when encountered a Terminal Node
            if isinstance(value, TerminalNode):
                for payoff in value.payoffs:
                    print('{:^10}'.format(bcolors.HEADER + bcolors.BOLD + '(' + str(player) + '=' + str(payoff) + ')'
                                          + bcolors.ENDC), end=' ')
                    player = 2
            num = 0
            # after the print of the payoffs we search for the parent of the node in order to have a clear
            # visualization of the reached level
            print('')
            while num < level:
                print('{:>15}'.format(' |'), end='')
                num += 1
    else:
        return


def visualize_infoset(el, infoset, level):
    # printing the name of the infoset
    if level == 1:
        print(bcolors.WARNING + 'Printing ' + infoset.name + bcolors.ENDC)
    # the printing follows the structure of the tree
    # doing a depth-first search of the nodes of a specific infoset
    if el.children is not None:
        for key, value in el.children.items():
            for node_level in infoset.info_nodes.values():
                # the node is found comparing the history of the nodes of an infoset with the current node's history
                # if they coincide, the node is found and printed
                if node_level.history[0:level] == value.history[0:]:
                    # the printing of the infoset is different depending of the input given to the function:
                    # 1 - original infoset of the extensive form representation
                    # 2 - infoset of the generated abstraction of the extensive form representation

                    #######################################################################
                    # print for abstraction
                    if '+' in in_chars(infoset.name):
                        # whenever the nodes of the infoset are reached, their entity is highlighted
                        if len(infoset.name.split('+')[0].split('/')[1:]) == level:
                            print('{:<15}'.format(bcolors.BOLD + bcolors.FAIL + '[' + value.history[-1] + ']'),
                                  end='' + bcolors.ENDC)
                        else:
                            print('{:<15}'.format(value.history[-1] + '  ->'), end='')
                        if len(infoset.name.split('+')[0].split('/')[1:]) > level:
                            # recursive call for the current node's children
                            visualize_infoset(value, infoset, level + 1)
                    #######################################################################
                    # print for no abstraction
                    else:
                        # whenever the nodes of the infoset are reached, their entity is highlighted
                        if len(infoset.name.split('/')[1:]) == level:
                            print('{:<15}'.format(bcolors.BOLD + bcolors.FAIL + '[' + value.history[-1] + ']'),
                                  end='' + bcolors.ENDC)
                        else:
                            print('{:<15}'.format(value.history[-1] + '  ->'), end='')
                        if len(infoset.name.split('/')[1:]) > level:
                            # recursive call for the current node's children
                            visualize_infoset(value, infoset, level + 1)
                    #######################################################################

                    num = 0
                    print('')
                    while num < level - 1:
                        print('{:>15}'.format(' |'), end='')
                        num += 1
    else:
        return


def visualize_info_structure(tree, infostructure):
    # each single infoset list, for each player is printed
    print(bcolors.BOLD + bcolors.UNDERLINE + 'Printing Information Sets of Player 1' + bcolors.ENDC)
    for info_set in infostructure.info_sets1:
        visualize_infoset(tree, info_set, 1)
    print(bcolors.BOLD + bcolors.UNDERLINE + '\n\nPrinting Information Sets of Player 2' + bcolors.ENDC)
    for info_set in infostructure.info_sets2:
        visualize_infoset(tree, info_set, 1)


def visualize_regrets(regrets_history):

    optimal_regrets = json_regrets_reader()
    regrets_difference = np.asarray(regrets_history) - np.asarray(optimal_regrets)

    plt.figure()
    plt.plot(regrets_difference, 'r')
    plt.show()
