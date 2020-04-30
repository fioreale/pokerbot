import logging

from working_tools.abstraction_generator import tree_navigator


def create_clustering_table(root, tree_level_number):
    create_clustering_table_logger = logging.getLogger('pokerbot')

    # dictionary to store the payoff space of the infosets
    cluster_table = {}

    # function to retrieve the infosets of a level
    print('computing infosets of level: ' + str(tree_level_number))
    infosets_list = tree_navigator.get_infosets_of_tree_level(root, tree_level_number)

    infosets_list = tree_navigator.infoset_group_filtering(infosets_list)

    # fill the dictionary
    for history_group in infosets_list:
        # compute all the strategies that follows a node in a infoset history group, this list of strategies allows us
        # to have an order of computation while retrieving the payoffs. It is necessary to retrieve the payoffs in the
        # same order because we need to have coherent payoff vector for all the infosets
        the_wonderful_magnificent_chosen_node = None
        for infoset in history_group:
            for node in infoset.info_nodes.values():
                # check that both player have different cards in order to obtain all the possible strategies.
                # (if both player have the same card the middle chance node won't have all the possible cards)
                same_cards_condition = node.history[0].split(':')[-1][0] == node.history[0].split(':')[-1][1]
                if not same_cards_condition:
                    the_wonderful_magnificent_chosen_node = node
                    create_clustering_table_logger.info('chosen node: %s', ''.join(the_wonderful_magnificent_chosen_node.history))
        # list used to store the list of strategies. These strategies define an order to visit the tree in order to
        # have a consistent payoff vector for each infoset
        strategies_list = the_wonderful_magnificent_chosen_node.compute_strategies_to_terminal_nodes()
        # delete first element from each strategy in order to "generalize" them and use them in each infoset
        strategies_list = list(map(lambda x: x[tree_level_number:], strategies_list))
        history_group_name = "".join(history_group[0].name[4:])
        cluster_table[history_group_name] = {}

        max_number_of_terminal_nodes = 0

        # compute the max number of terminal nodes in infoset
        for infoset in history_group:
            computed_number = infoset.compute_number_of_terminal_nodes()
            if computed_number > max_number_of_terminal_nodes:
                max_number_of_terminal_nodes = computed_number

        terminal_node_difference = 0

        for infoset in history_group:
            computed_number = infoset.compute_number_of_terminal_nodes()
            if computed_number < max_number_of_terminal_nodes:
                terminal_node_difference = max_number_of_terminal_nodes - computed_number
            create_clustering_table_logger.info('infoset in history group: %s', infoset.name)
            create_clustering_table_logger.info('history_group_name: %s', history_group_name)
            # compute the payoff of each infoset

            cluster_table[history_group_name][infoset] = tree_navigator.compute_payoff_coordinates(infoset,
                                                                                                   strategies_list,
                                                                                                   terminal_node_difference)
    return cluster_table
