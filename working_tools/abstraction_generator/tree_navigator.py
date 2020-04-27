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
    # list used to store the information sets of the level
    infosets_collection_list = []

    # if we have to explore more than one level the function is called on the child
    if level > 1:
        # iterate over all the children to recursively call the function on each child
        for child in root.children.values():
            collected_infosets = get_infosets_of_tree_level(child, level - 1)
            for infoset in collected_infosets:
                if infoset not in infosets_collection_list:
                    infosets_collection_list.append(infoset)
        return infosets_collection_list
    else:
        for node in root.children.values():
            if node.infoset not in infosets_collection_list:
                infosets_collection_list.append(node.infoset)
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


def compute_payoff_coordinates(infoset):
    # first node of the infoset used to compute the strategies for all the infosets
    # it is sufficient to consider the first node of one infoset because all the nodes inside the same infoset have the
    # same possible strategies
    first_node = list(infoset.info_nodes.values())[0]
    # list used to store the list of strategies. These strategies define an order to visit the tree in order to have a
    # consistent payoff vector for each infoset
    strategies_list = first_node.compute_strategies_to_terminal_nodes()
    # delete first element from each strategy in order to "generalize" them and use them in each infoset
    strategies_list = list(map(lambda x: x[1:], strategies_list))
    # payoff vector contains the coordinates (i.e. the utilities) to position the infoset in the payoff space
    payoff_vector = []
    # iterate over all the nodes of the infoset and retrieve the payoff vector
    for node in infoset.info_nodes.values():
        payoff_vector.extend(node.compute_payoff_coordinate_vector(node.player, strategies_list))
    return payoff_vector
