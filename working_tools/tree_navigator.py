# old code used to reverse the dictionary used to build the cluster table
def search_node(dictionary, utility):
    nodes_list = []
    for index_node, index_action, index_utility in dictionary.items():
        if dictionary[index_node, index_action] == utility:
            nodes_list.append(index_node)
    return nodes_list
