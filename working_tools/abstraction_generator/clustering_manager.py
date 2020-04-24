import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def create_clustering_table(node_list):
    # dictionary indexed by action and utility that stores every node that can return that utility
    cluster_table = {}
    # cycle through each children of the root, saves the list of nodes for the utlities of that action
    for node in node_list:
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

def create_clustering_table_new(node_list):
    # dictionary indexed by action and utility that stores every node that can return that utility
    cluster_table = {}
    # cycle through each children of the root, saves the list of nodes for the utlities of that action
    for node in node_list:
        for action in node.actions:
            index = 0
            if node.player == '1':
                index = 0
            else:
                index = 1
            # action contains

            computed_utility = int(node.children['P' + node.player + ':' + action].compute_metrics())
            if (action, computed_utility) not in cluster_table.keys():
                cluster_table[(action, computed_utility)] = []
                cluster_table[(action, computed_utility)].append(node)
            else:
                cluster_table[(action, computed_utility)].append(node)

    return cluster_table



def print_cluster_table(cluster_table):

    # list of list containing all the coordinates for each axis.
    axes_list = []

    # list of action where we save the distinct values of actions ordered to create the coordinates in the same order
    distinct_actions_order = []

    # list of labels for each point
    labels = []

    # cycle to create the list of ordered distinct values of actions
    for action, utility in cluster_table.keys():
        if action not in distinct_actions_order:
            distinct_actions_order.append(action)
            axes_list.append(list())

    # cycle to create the lists of coordinates and distinct labels
    for (action, utility), node_list in cluster_table.items():
        for node in node_list:
            axes_list[distinct_actions_order.index(action)].append(float(utility) / 1000000)
            if node.history not in labels:
                labels.append(node.history)

    # draw point based on above x, y and z (optional) axis values
    if len(distinct_actions_order) == 2:
        fig, ax = plt.subplots()
        ax.scatter(axes_list[0], axes_list[1])
        ax.set_xlabel(distinct_actions_order[0])
        ax.set_ylabel(distinct_actions_order[1])
    else:
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(axes_list[0], axes_list[1], axes_list[2])
        ax.set_xlabel(distinct_actions_order[0])
        ax.set_ylabel(distinct_actions_order[1])
        ax.set_zlabel(distinct_actions_order[2])

    # set points labels based on above x, y and z (optional) axis values
    labels_concatenation_dict = {}

    if len(distinct_actions_order) == 2:

        for i, x_utility in enumerate(axes_list[0]):
            y_utility = axes_list[1][i]
            if (x_utility, y_utility) in labels_concatenation_dict.keys():
                labels_concatenation_dict[(x_utility, y_utility)] += labels[i]
            else:
                labels_concatenation_dict[(x_utility, y_utility)] = labels[i]

        for i in range(0, len(labels)):
            ax.annotate(labels_concatenation_dict[axes_list[0][i], axes_list[1][i]], (axes_list[0][i], axes_list[1][i]))

    else:

        for i, x_utility in enumerate(axes_list[0]):
            y_utility = axes_list[1][i]
            z_utility = axes_list[2][i]
            if (x_utility, y_utility, z_utility) in labels_concatenation_dict.keys():
                labels_concatenation_dict[(x_utility, y_utility, z_utility)] += labels[i]
            else:
                labels_concatenation_dict[(x_utility, y_utility, z_utility)] = labels[i]

        for i in range(0, len(labels)):
            ax.text(axes_list[0][i], axes_list[1][i], axes_list[2][i],
                    labels_concatenation_dict[axes_list[0][i], axes_list[1][i], axes_list[2][i]])

    # Set chart title
    plt.title("Cluster Table")
    plt.show()
