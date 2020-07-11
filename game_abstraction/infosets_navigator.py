from game_model.terminal_node import TerminalNode


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
