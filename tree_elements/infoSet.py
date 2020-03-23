
class InfoSet:  # list of nodes for each information set
    def __init__(self):
        self.name = None
        self.info_nodes = {}             # all the nodes of the tree being part of it

    def create_info_set(self, history, nodes, root):
        self.name = history
        nodes_list = nodes.split(' ')
        for node in nodes_list:
            path = node.split('/')[1:]
            self.info_nodes[node] = root.node_finder(path)
            self.info_nodes[node].infoSet = self

        return self
