# list of nodes for each information set


class InfoSet:
    def __init__(self):
        # the name of the infoset is the complete history path that leads to the infoset
        self.name = None
        # info_nodes is a dictionary indexed by node paths and containing the node objects of the corresponding nodes
        # Example: {['/C:99/P1:c/P2:c/C:T/P1:raise4' : <object ActionNode>]}
        self.info_nodes = {}

    # function that build the infoset
    # history contains the path that leads to the infoset with partial information.
    # Example: '/?9/P1:c/P2:c/C:T/P1:raise4'
    # nodes contains the list of paths that leads to the nodes of the infoset.
    # Example: '/C:99/P1:c/P2:c/C:T/P1:raise4 /C:T9/P1:c/P2:c/C:T/P1:raise4 ...'
    # root contains the root node of the tree
    def create_info_set(self, history, nodes, root):
        # the name of the infoset is initialized with the complete history that leads to the infoset
        if history[1] == 'C':
            self.name = history.replace('/C:', '/', 1)
        else:
            self.name = history
        # nodes_list contains all the nodes paths in the infoset passed through the attribute nodes
        nodes_list = nodes.split(' ')
        for node in nodes_list:
            # path is the list of nodes that leads to the node in the infoset
            path = node.split('/')[1:]  # the first element id discarded because it is an empty string
            # the dictionary of nodes in the infoset is filled with the node path index
            # and the corresponding node object
            self.info_nodes[node] = root.node_finder(path)
            # the current infoset is assigned to Node.infoset attribute of every node in the current infoset
            self.info_nodes[node].infoset = self

        return self

    def compute_number_of_terminal_nodes(self):
        number_of_terminal_nodes = 0
        for node in self.info_nodes.values():
            number_of_terminal_nodes += node.compute_number_of_terminal_nodes()
        return number_of_terminal_nodes
