from pokerbot import FILE_NAME
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
    # if we have to explore more than one level the function is called on the child
    if remaining_levels > 1:
        # iterate over all the children to recursively call the function on each child
        collected_infosets = []
        for child in root.children.values():
            # retrieve infosets returned by children of the node
            collected_infosets.extend(get_infosets_of_tree_level(child, remaining_levels - 1))
        return list(set(collected_infosets))
    else:
        # since we don't have to explore any more levels the function is not recursively called anymore
        # iterate over the children of the current node
        child_infosets = []
        for node in root.children.values():
            is_chance_node = (node.player == 'C')
            is_terminal_node = isinstance(node, TerminalNode)
            if (not is_chance_node) and (not is_terminal_node):
                child_infosets.append(node.infoset)
        return child_infosets


def get_descendants(infoset):
    descendants = []
    infoset_player = list(infoset.info_nodes.values())[0].player
    for node in infoset.info_nodes.values():
        descendants.extend(get_descendants_of_infoset(node, infoset_player, 0))
    descendants = set(descendants)
    return descendants


def get_descendants_of_infoset(root, infoset_player, iteration_number):
    infoset_collection = []
    current_infoset_player = root.player
    if iteration_number == 0 or current_infoset_player != infoset_player:
        for child in root.children.values():
            # node_collection.append(get_tree_level(child, level - 1))
            descendants = get_descendants_of_infoset(child, infoset_player, iteration_number + 1)
            if isinstance(descendants, list):
                infoset_collection.extend(descendants)
            else:
                infoset_collection.append(descendants)
        return infoset_collection
    elif current_infoset_player == infoset_player:
        return root.infoset
    else:
        return


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
                if same_history_group_infosets[0].name.split('/')[2:] == new_infoset.name.split('/')[2:]:
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


def compute_payoff_coordinates(infoset, nodes_letter_list, strategies_list,
                               difference_of_terminal_nodes):
    # payoff vector contains the coordinates (i.e. the utilities) to position the infoset in the payoff space
    payoff_vector = []
    # iterate over all the nodes of the infoset and retrieve the payoff vector
    if FILE_NAME == 'kuhn.txt':
        for node in infoset.info_nodes.values():
            payoff_vector.extend(node.compute_payoff_coordinate_vector(node.player,
                                                                       strategies_list,
                                                                       difference_of_terminal_nodes))
    else:
        for node_letter in nodes_letter_list:
            next_node_to_visit_string = '/C:' + str(infoset.name[1:]).replace('?', node_letter)
            if next_node_to_visit_string not in infoset.info_nodes.keys():
                payoff_vector.extend([0 for i in range(difference_of_terminal_nodes)])
            else:
                node = infoset.info_nodes[next_node_to_visit_string]
                # compute payoff vector on every strategy
                payoff_vector.extend(node.compute_payoff_coordinate_vector(node.player,
                                                                           strategies_list,
                                                                           difference_of_terminal_nodes))

    return payoff_vector

