from working_tools.abstraction_generator import tree_navigator


def create_clustering_table(root, tree_level_number):

    # dictionary to store the payoff space of the infosets
    cluster_table = {}

    # function to retrieve the infosets of all the nodes in a level
    infosets_list = tree_navigator.get_infosets_of_tree_level(root, tree_level_number)

    # function to filter the infosets and group them by corresponding history
    infosets_list = tree_navigator.infoset_group_filtering(infosets_list)

    # iteration over the history groups to fill the dictionary
    for history_group in infosets_list:

        strategies_list = strategies_list_calculator(history_group, tree_level_number)

        history_group_name = "".join(history_group[0].name[4:])
        cluster_table[history_group_name] = {}

        max_number_of_terminal_nodes, max_number_of_info_nodes = max_numbers_calculator(history_group)

        infoset_with_max_nodes = max_nodes_infoset_finder(history_group, max_number_of_info_nodes)

        # list used to store the list of nodes. These nodes define an order to visit the tree infoset to
        # have a consistent payoff vector for each infoset
        nodes_letter_list = nodes_letter_list_calculator(infoset_with_max_nodes)

        for infoset in history_group:
            difference_of_terminal_nodes = max_number_of_terminal_nodes - infoset.compute_number_of_terminal_nodes()

            # compute the payoff of each infoset
            cluster_table[history_group_name][infoset] = tree_navigator.\
                compute_payoff_coordinates(infoset,
                                           nodes_letter_list,
                                           strategies_list,
                                           difference_of_terminal_nodes)
    return cluster_table


def max_numbers_calculator(history_group):
    max_number_of_info_nodes = 0
    max_number_of_terminal_nodes = 0

    # compute the max number of terminal nodes in infoset and max number of info nodes in an infoset
    for infoset in history_group:
        computed_number = len(infoset.info_nodes)
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


def nodes_letter_list_calculator(infoset_with_max_nodes):
    # list used to store the list of nodes. These nodes define an order to visit the tree infoset to
    # have a consistent payoff vector for each infoset
    nodes_letter_list = []

    if infoset_with_max_nodes.name[1] == '?':
        for node in infoset_with_max_nodes.info_nodes.keys():
            nodes_letter_list.append(node[3])
    else:
        for node in infoset_with_max_nodes.info_nodes.keys():
            nodes_letter_list.append(node[4])

    return nodes_letter_list


def strategies_list_calculator(history_group, tree_level_number):
    # compute all the strategies that follows a node in a infoset history group, this list of strategies allows us
    # to have an order of computation while retrieving the payoffs. It is necessary to retrieve the payoffs in the
    # same order because we need to have coherent payoff vector for all the infosets
    node_with_no_double_cards = None
    for infoset in history_group:
        for node in infoset.info_nodes.values():
            # check that both player have different cards in order to obtain all the possible strategies.
            # (if both player have the same card the middle chance node won't have all the possible cards)
            same_cards_condition = node.history[0].split(':')[-1][0] == node.history[0].split(':')[-1][1]
            if not same_cards_condition:
                node_with_no_double_cards = node

    # list used to store the list of strategies. These strategies define an order to visit the tree in order to
    # have a consistent payoff vector for each infoset
    strategies_list = node_with_no_double_cards.compute_strategies_to_terminal_nodes()
    # delete first element from each strategy in order to "generalize" them and use them in each infoset
    strategies_list = list(map(lambda x: x[tree_level_number:], strategies_list))

    return strategies_list
