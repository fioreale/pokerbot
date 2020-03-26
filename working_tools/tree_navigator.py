def get_tree_level(root, level):
    if level == 0:
        return root

    node_collection = []
    if level > 1:
        for child in root.children.values():
            # node_collection.append(get_tree_level(child, level - 1))
            node_collection += get_tree_level(child, level - 1)
        return node_collection
    else:
        return root.children.values()


def split_node_list(node_list):
    set_of_actions = list()
    set_of_nodes = list()
    for node in node_list:
        if node.actions not in set_of_actions:
            set_of_actions.append(node.actions)
            set_of_nodes.append(list())
    for node in node_list:
        set_of_nodes[set_of_actions.index(node.actions)].append(node)
    return set_of_nodes


def find_tree_height(node, level):
    max_level = level
    if node.children is not None:
        for child in node.children.values():
            value = find_tree_height(child, level + 1)
            if max_level < value:
                max_level = value
    return max_level
