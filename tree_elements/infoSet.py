from tree_elements.node import Node
from tree_elements.nature_node import NatureNode
from tree_elements.action_node import ActionNode
from tree_elements.terminal_node import TerminalNode

class InfoSet:  # list of nodes for each information set
    def __init__(self):
        self.name = None
        self.infoNodes = {}             # all the nodes of the tree being part of it

    def createInfoSet(self, history, nodes, root):
        self.name = history
        nodes_list = nodes.split(' ')
        for node in nodes_list:
            path = node.split('/')[1:]
            self.infoNodes[node] = root.node_finder(path)
            self.infoNodes[node].infoSet = self.name
        return self
