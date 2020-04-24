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
        self.utilities = {}     # utilities dictionary used  to compute backward induction outcomes
        self.utilities_per_action = {}  # dictionary where we save all the possible utilities for each single action
        # reference Abstraction_Generation.pdf slide 23/67

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

    # function used to perform backward induction
    # TODO delete this function
    def compute_utilities(self):
        max_utility = [0.0, 0.0]
        # cycle through each action to retrieve the child node utilities
        # returned utilities are a list [utility_player_1, utility_player_2]
        for action in self.actions:
            self.utilities[action] = self.children['P' + self.player + ':' + action].compute_utilities()
        # initialization of the list max_utility where  we're gonna save the best utility for this node
        max_utility = self.utilities[self.actions[0]]
        # cycle through the computed utilities to compute the best one
        for key, utility in self.utilities.items():
            # computation of best utility for first player
            if self.player == '1':
                if float(utility[0]) > max_utility[0]:
                    max_utility = utility
            # computation of best utility for second player
            if self.player == '2':
                if float(utility[1]) > max_utility[1]:
                    max_utility = utility
        # returns best utility which is a vector [utility_player_1, utility_player_2]
        return max_utility
