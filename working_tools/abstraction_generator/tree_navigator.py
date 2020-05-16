from pokerbot import FILE_NAME


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
