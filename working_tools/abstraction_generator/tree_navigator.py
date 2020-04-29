from tree_elements.terminal_node import TerminalNode


def get_tree_level(root, level):
    if level == 0:
        return [root]

    node_collection = []
    if level > 1:
        for child in root.children.values():
            # node_collection.append(get_tree_level(child, level - 1))
            node_collection += get_tree_level(child, level - 1)
        return node_collection
    else:
        for node in root.children.values():
            node_collection += [node]
        return node_collection


def get_infosets_of_tree_level(root, level):
    # matrix used to store the information sets of the level. It is organized in same_history_groups and each history
    # group contains a list of infosets
    infosets_collection_list = []

    # if we have to explore more than one level the function is called on the child
    if level > 1:
        # iterate over all the children to recursively call the function on each child
        for child in root.children.values():
            # retrieve infosets returned by children of the node
            collected_infosets = get_infosets_of_tree_level(child, level - 1)
            # iterate over the newly collected infosets lists
            for new_infoset_history_group in collected_infosets:
                # iterate over the newly collected infosets
                for new_infoset in new_infoset_history_group:
                    # boolean variable to check that infoset has not been inserted
                    inserted = False
                    # check if list is empty
                    if not infosets_collection_list:
                        infosets_collection_list.append([new_infoset])
                    else:
                        # iterate over the history_groups
                        for same_history_group_infosets in infosets_collection_list:
                            # check that the new infoset belong to the same history group
                            if same_history_group_infosets[0].name.split('/')[2:] == new_infoset.name.split('/')[2:]:
                                # check if the infosets has not already been inserted
                                if new_infoset not in same_history_group_infosets:
                                    # add the new infoset to the history group
                                    same_history_group_infosets.append(new_infoset)
                                    inserted = True
                        if not inserted:
                            infosets_collection_list.append([new_infoset])
        return infosets_collection_list
    else:
        # since we don't have to explore any more levels the function is not recursively called anymore
        # iterate over the children of the current node
        child_infosets = []
        for node in root.children.values():
            is_chance_node = node.player == 'C'
            is_terminal_node = isinstance(node, TerminalNode)
            if (node.infoset not in child_infosets) and (not is_chance_node) and (not is_terminal_node):
                child_infosets.append(node.infoset)
        infosets_collection_list.append(child_infosets)
        return infosets_collection_list


def split_node_list(node_list):
    set_of_actions = list()
    sets_of_nodes = list()
    for node in node_list:
        if node.actions not in set_of_actions:
            set_of_actions.append(node.actions)
            sets_of_nodes.append(list())
    for node in node_list:
        sets_of_nodes[set_of_actions.index(node.actions)].append(node)
    return sets_of_nodes


def find_tree_height(node, level):
    max_height = level
    if node.children is not None:
        for child in node.children.values():
            found_height = find_tree_height(child, level + 1)
            if max_height < found_height:
                max_height = found_height
    return max_height


def compute_payoff_coordinates(infoset, strategies_list):
    # payoff vector contains the coordinates (i.e. the utilities) to position the infoset in the payoff space
    payoff_vector = []
    # iterate over all the nodes of the infoset and retrieve the payoff vector
    for node in infoset.info_nodes.values():
        # check if we're computing the payoff of a node with the same card dealt to every player
        if node.history[0].split(':')[-1][0] == node.history[0].split(':')[-1][1]:
            # build the string of the card that is not possible to draw
            impossible_card_string = 'C:' + node.history[0].split(':')[-1][0]
            # sanitize the strategies from strategies that are not possible due to impossible card to be drawn
            cleaned_strategies_list = list(filter(lambda x: impossible_card_string not in x, strategies_list))
            # compute payoff vector on sanitized strategies
            payoff_vector.extend(node.compute_payoff_coordinate_vector(node.player, cleaned_strategies_list))
        else:
            # compute payoff vector on every strategy
            payoff_vector.extend(node.compute_payoff_coordinate_vector(node.player, strategies_list))
    return payoff_vector


def compress_tree(infosets, cluster_table):
    return
