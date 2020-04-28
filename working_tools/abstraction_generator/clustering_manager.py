from working_tools.abstraction_generator import tree_navigator


def create_clustering_table(root, tree_level_number):
    # dictionary to store the payoff space of the infosets
    cluster_table = {}

    # function to retrieve the infosets of a level
    infosets_list = tree_navigator.get_infosets_of_tree_level(root, tree_level_number)

    # fill the dictionary
    for history_group in infosets_list:
        history_group_name = "".join(history_group[0].name.split('/')[2:])
        cluster_table[history_group_name] = {}
        for infoset in history_group:
            # compute the payoff of each infoset
            cluster_table[history_group_name][infoset] = tree_navigator.compute_payoff_coordinates(infoset)
    return cluster_table
