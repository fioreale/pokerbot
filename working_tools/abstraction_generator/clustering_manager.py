from working_tools.abstraction_generator import tree_navigator


def create_clustering_table(root):
    # dictionary to store the payoff space of the infosets
    cluster_table = {}

    # function to retrieve the infosets of a level
    # TODO retrieve only correlated infosets, namely infosets which have same history of actions
    infosets_list = tree_navigator.get_infosets_of_tree_level(root, 1)

    # fill the dictionary
    for infoset in infosets_list:
        # compute the payoff of each infoset
        cluster_table[infoset] = tree_navigator.compute_payoff_coordinates(infoset)
    return cluster_table
