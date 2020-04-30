import logging

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


def get_infosets_of_tree_level(root, remaining_levels):
    get_infosets_of_tree_level_logger = logging.getLogger('pokerbot')

    get_infosets_of_tree_level_logger.info('computing infoset of level: %d', remaining_levels)
    # if we have to explore more than one level the function is called on the child
    if remaining_levels > 1:
        # iterate over all the children to recursively call the function on each child
        collected_infosets = []
        for child in root.children.values():
            # retrieve infosets returned by children of the node
            get_infosets_of_tree_level_logger.info('collecting infosets from node: %s', ''.join(child.history))
            collected_infosets.extend(get_infosets_of_tree_level(child, remaining_levels - 1))
            # iterate over the newly collected infosets lists
        return collected_infosets
    else:
        get_infosets_of_tree_level_logger.info('last level nodes')
        # since we don't have to explore any more levels the function is not recursively called anymore
        # iterate over the children of the current node
        child_infosets = []
        for node in root.children.values():
            is_chance_node = (node.player == 'C')
            is_terminal_node = isinstance(node, TerminalNode)
            if is_chance_node:
                get_infosets_of_tree_level_logger.info('is Chance Node')
            elif is_terminal_node:
                get_infosets_of_tree_level_logger.info('is Terminal Node')
            else:
                child_infosets.append(node.infoset)
                get_infosets_of_tree_level_logger.info('collected infoset from child nodes: %s', node.infoset.name)
        return child_infosets


def infoset_group_filtering(list_of_infosets):
    # matrix used to store the information sets of the level. It is organized in same_history_groups and each history
    # group contains a list of infosets
    infosets_collection_list = []

    for new_infoset in set(list_of_infosets):
        if not infosets_collection_list:
            infosets_collection_list.append([new_infoset])
        else:
            inserted = False
            for same_history_group_infosets in infosets_collection_list:
                history_group_name_no_chance_node = list(filter(lambda x: 'C' not in x,
                                                                same_history_group_infosets[0].name.split('/')[2:]))
                new_infoset_name_no_chance_node = list(filter(lambda x: 'C' not in x,
                                                              new_infoset.name.split('/')[2:]))
                if history_group_name_no_chance_node == new_infoset_name_no_chance_node:
                    same_history_group_infosets.append(new_infoset)
                    inserted = True
            if not inserted:
                infosets_collection_list.append([new_infoset])

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


def compute_payoff_coordinates(infoset, strategies_list, difference_of_number_of_nodes):
    # payoff vector contains the coordinates (i.e. the utilities) to position the infoset in the payoff space
    payoff_vector = []
    # iterate over all the nodes of the infoset and retrieve the payoff vector
    for node in infoset.info_nodes.values():
        # compute payoff vector on every strategy
        payoff_vector.extend(node.compute_payoff_coordinate_vector(node.player, strategies_list,
                                                                   difference_of_number_of_nodes))

    return payoff_vector


def compress_tree(infosets, cluster_table):
    return
