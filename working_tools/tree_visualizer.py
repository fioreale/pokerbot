from tree_elements.terminal_node import TerminalNode


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def visualize_game_tree(el, level):
    if el.children is not None:
        for key, value in el.children.items():
            print('{:<15}'.format(value.history[-1] + '  ->'), end='')
            visualize_game_tree(value, level + 1)
            player = 1
            if isinstance(value, TerminalNode):
                for payoff in value.payoffs:
                    print('{:^10}'.format(bcolors.HEADER + bcolors.BOLD + '(' + str(player) + '=' + str(payoff) + ')'
                                          + bcolors.ENDC), end=' ')
                    player = 2
            num = 0
            print('')
            while num < level:
                print('{:>15}'.format(' |'), end='')
                num += 1
    else:
        return


def visualize_infoset(el, infoset, level):
    if level == 1:
        print(bcolors.WARNING + 'Printing ' + infoset.name + bcolors.ENDC)
    if el.children is not None:
        for key, value in el.children.items():
            for node_level in infoset.info_nodes.values():
                if node_level.history[0:level] == value.history[0:]:
                    if len(infoset.name.split('/')[1:]) == level:
                        print('{:<15}'.format(bcolors.BOLD + bcolors.FAIL + '[' + value.history[-1] + ']'),
                              end='' + bcolors.ENDC)
                    else:
                        print('{:<15}'.format(value.history[-1] + '  ->'), end='')
                    if len(infoset.name.split('/')[1:]) > level:
                        visualize_infoset(value, infoset, level + 1)
                    num = 0
                    print('')
                    while num < level-1:
                        print('{:>15}'.format(' |'), end='')
                        num += 1
            # if value.history[-1]:
            #     print('{:<15}'.format(bcolors.OKBLUE + value.history[-1] + bcolors.ENDC), end='')
            # else:
            #     print('{:<15}'.format(value.history[-1] + '  ->'), end='')

    else:
        return


def visualize_info_structure(tree, infostructure):
    print(bcolors.BOLD + bcolors.UNDERLINE + 'Printing Information Sets of Player 1' + bcolors.ENDC)
    for info_set in infostructure.info_sets1:
        visualize_infoset(tree, info_set, 1)
    print(bcolors.BOLD + bcolors.UNDERLINE + '\n\nPrinting Information Sets of Player 2' + bcolors.ENDC)
    for info_set in infostructure.info_sets2:
        visualize_infoset(tree, info_set, 1)
