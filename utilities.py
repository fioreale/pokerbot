from tree_elements.terminal_node import TerminalNode
import matplotlib.pyplot as plt


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
                for payoff in value.payoffs:
                    print('{:^10}'.format(bcolors.HEADER + bcolors.BOLD + '(' + str(player) + '=' + str(payoff) + ')' + bcolors.ENDC), end=' ')
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
            for node_level in infoset.infoNodes.values():
                if node_level.history[0:level] == value.history[0:]:
                    if len(infoset.name.split('/')[1:]) == level:
                        print('{:<15}'.format(bcolors.BOLD + bcolors.FAIL + '[' + value.history[-1] + ']'), end='' + bcolors.ENDC)
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

def visualize_InfoStructure(tree, infostruscture):
    print(bcolors.BOLD + bcolors.UNDERLINE + 'Printing Information Sets of Player 1' + bcolors.ENDC)
    for info_set in infostruscture.infoSets1:
        visualize_infoset(tree, info_set, 1)
    print(bcolors.BOLD + bcolors.UNDERLINE + '\n\nPrinting Information Sets of Player 2' + bcolors.ENDC)
    for info_set in infostruscture.infoSets2:
        visualize_infoset(tree, info_set, 1)


# function that builds the table where to compute the clusters
# returns a dictionary indexed per action and utility which returns a list of nodes
def clustering_table_creation(root):
    # dictionary indexed by action and utility that stores every node that can return that utility
    cluster_table = {}
    # cycle through each children of the root, saves the list of nodes for the utlities of that action
    for key, node in root.children.items():
        for action in node.actions:
            index = 0
            if node.player == '1':
                index = 0
            else:
                index = 1
            # action contains
            computed_utility = int(node.children['P' + node.player + ':' + action].compute_utilities()[index]*1000000)
            if (action, computed_utility) not in cluster_table.keys():
                cluster_table[(action, computed_utility)] = []
                cluster_table[(action, computed_utility)].append(node)
            else:
                cluster_table[(action, computed_utility)].append(node)

    return cluster_table
    # old code to reverse the dictionary
    # for node, action, utility in cluster_table.items():
    #   cluster_table[action, utility] = search_node(cluster_table, action, utility)


def print_cluster_table(cluster_table):

    # x axis value list.
    x_number_list = []

    # y axis value list.
    y_number_list = []

    n = []

    for (action, utility), node_list in cluster_table.items():
        if action == 'c':
            for node in node_list:
                x_number_list.append(float(utility)/1000000)
                n.append(node.history)

        if action == 'r' or action == 'raise2':
            for node in node_list:
                y_number_list.append(float(utility)/1000000)
                # n.append(node.history)

    fig, ax = plt.subplots()
    # Draw point based on above x, y axis values.
    ax.scatter(x_number_list, y_number_list)

    print(x_number_list)
    print(y_number_list)

    for i, txt in enumerate(n):
        print(i)
        print(txt)
        ax.annotate(txt, (x_number_list[i], y_number_list[i]))

    # Set chart title.
    # ax.title("Extract Number Root ")

    # Set x, y label text.
    # fig.xlabel("Number")
    # fig.ylabel("Extract Root of Number")
    plt.show()

# old code used to reverse the dictionary used to build the cluster table
def search_node(dictionary, action, utility):
    nodes_list = []
    for index_node, index_action, index_utility in dictionary.items():
        if dictionary[index_node, index_action] == utility:
            nodes_list.append(index_node)
    return nodes_list
