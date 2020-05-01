def max_numbers_calculator(history_group):
    max_number_of_info_nodes = 0
    max_number_of_terminal_nodes = 0

    # compute the max number of terminal nodes in infoset and max number of info nodes in an infoset
    for infoset in history_group:
        computed_number = len(infoset.info_nodes.values())
        if computed_number > max_number_of_info_nodes:
            max_number_of_info_nodes = computed_number
        computed_number = infoset.compute_number_of_terminal_nodes()
        if computed_number > max_number_of_terminal_nodes:
            max_number_of_terminal_nodes = computed_number

    return max_number_of_terminal_nodes, max_number_of_info_nodes


def max_nodes_infoset_finder(history_group, max_number_of_info_nodes):
    # retrieves one infoset with the max number of info nodes
    infoset_with_max_nodes = None

    for infoset in history_group:
        if len(infoset.info_nodes) == max_number_of_info_nodes:
            infoset_with_max_nodes = infoset

    return infoset_with_max_nodes