import matplotlib.pyplot as plt


# function that builds the table where to compute the clusters
# returns a dictionary indexed per action and utility which returns a list of nodes
# def clustering_table_creation(root):
#     # dictionary indexed by action and utility that stores every node that can return that utility
#     cluster_table = {}
#     # cycle through each children of the root, saves the list of nodes for the utlities of that action
#     for key, node in root.children.items():
#         for action in node.actions:
#             index = 0
#             if node.player == '1':
#                 index = 0
#             else:
#                 index = 1
#             # action contains
#             computed_utility = int(node.children['P' + node.player + ':' + action].compute_utilities()[index]*1000000)
#             if (action, computed_utility) not in cluster_table.keys():
#                 cluster_table[(action, computed_utility)] = []
#                 cluster_table[(action, computed_utility)].append(node)
#             else:
#                 cluster_table[(action, computed_utility)].append(node)
#
#     return cluster_table

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


def print_cluster_table(cluster_table):

    # x axis value list.
    x_number_list = []

    # y axis value list.
    y_number_list = []

    z_number_list = []

    n = []

    for (action, utility), node_list in cluster_table.items():
        if action == 'c':
            for node in node_list:
                x_number_list.append(float(utility)/1000000)
                n.append(node.history)

        if action == 'r' or action == 'raise2' or action == 'raise4':
            for node in node_list:
                y_number_list.append(float(utility)/1000000)
                # n.append(node.history)

        if action == 'f':
            for node in node_list:
                z_number_list.append(float(utility)/1000000)
                # n.append(node.history)

    fig, ax = plt.subplots()
    # Draw point based on above x, y axis values.
    # if len(x_number_list)!= 0 and len(y_number_list) != 0 and len(z_number_list) != 0:
    #     ax.scatter(x_number_list, y_number_list, z_number_list)
    # else :
    #     ax.scatter(x_number_list, y_number_list)
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
