from tree_elements.terminal_node import TerminalNode

def in_chars(string):
    return [char for char in string]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def visualize(el, level):
    if el.children is not None:
        for key, value in el.children.items():
            print('{:<15}'.format(value.history[-1] + '  ->'), end='')
            visualize(value, level+1)
            player = 1
            if isinstance(value, TerminalNode):
                for payoff in value.payoffs.values():
                    print('{:^10}'.format(bcolors.HEADER + bcolors.BOLD + '(' + str(player) + '=' + str(payoff) + ')' + bcolors.ENDC), end=' ')
                    player = 2
            num = 0
            print('')
            while num < level:
                print('{:>15}'.format(' |'), end='')
                num += 1
    else:
        return