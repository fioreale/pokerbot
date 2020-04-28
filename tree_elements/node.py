import numpy as np


class Node:
    def __init__(self):
        # history list where there is the sequence of nodes that leads to the current node
        # Example: ['C:99', 'P1:raise2', 'P2:raise2', 'P1:c']
        self.history = []
        # list of possible actions to be perform by node player
        # Example: ['c', 'f']
        self.actions = []
        # dictionary of children indexed by children node name which stores values of the node object
        # Example: {['C:99' : <object ActionNode>; ... ]}
        self.children = {}
        # variable where we save the parent node
        self.parent = None
        # variable where we save the infoset to which this node belongs
        self.infoset = None
        # variable where we save the player that plays in this node
        self.player = None
        self.utilities = {}  # utilities dictionary used  to compute backward induction outcomes
        self.utilities_per_action = {}  # dictionary where we save all the possible utilities for each single action
        # reference Abstraction_Generation.pdf slide 23/67
        self.action_value = None

    # recursive function that traverse the history and returns its last node
    # history contains the list of nodes that leads to the node to find, the last node of the list is the node
    # to find. Example: ['C:99', 'P1:raise2', 'P2:raise2', 'P1:c']
    def node_finder(self, history):
        # when the parameter history is empty it means that we have reached the desired node
        if len(history) == 0:
            return self
        # if the history is not empty we search through the child of the current node
        else:
            # we select the next node to search
            children_node_to_follow = history[0]
            # we update the history by removing the first element
            updated_history = history[1:]
            # we call the recursive function on the next node
            return self.children[children_node_to_follow].node_finder(updated_history)

    def append_child(self, node, history):
        self.children[history[-1]] = node

    # abstract
    def compute_strategies_to_terminal_nodes(self):
        return

    # abstract
    def compute_payoff_coordinate_vector(self, player, strategies_list):
        return

    # TODO
    def compress_tree(self, cluster_table, kmeans):
        for kmeans_labels in set(kmeans.labels_):
            infosets_list = list(cluster_table.keys())
            same_label_infosets_indexes = np.argwhere(kmeans.labels_ == kmeans_labels)
            # group all infosets with same labels
            same_label_infosets_ndarray = np.array(infosets_list)[same_label_infosets_indexes]
            same_label_infosets_list = list(same_label_infosets_ndarray)
            for infoset in infosets_list[1:]:
                infosets_list[0].info_nodes.append(infoset.info_nodes)
                infoset.info_nodes = []
