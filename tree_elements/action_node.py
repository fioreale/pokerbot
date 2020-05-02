from tree_elements.nature_node import NatureNode
from tree_elements.node import Node


# class used to build nodes where players chose which action to play
# extends superclass Node


class ActionNode(Node):
    def __init__(self):
        Node.__init__(self)

    # initialization method of the class where we set up the attributes values
    # history contains the path of nodes that leads to the node to be created
    # Example: '/C:99/P1:raise2/P2:raise2/P1:c'
    # player contains the number of the player. Example: '1'
    # actions contains a list of actions available for the player of the node. Example: 'c f'
    # root is the root node of the tree
    def create_action_node(self, history, player, actions, root):
        # history contains a list of string that identifies the nodes that leads to the current node
        # the first element is discarded because it is an empty string
        history_list = history.split('/')[1:]
        # the list of nodes is saved in the local history variable
        self.history = history_list
        # to retrieve the parent of the current node we perform a search through the game tree
        # the last element of the tree is discarded because it is the current node, we need the father
        self.parent = root.node_finder(history_list[:-1])
        # the current node is added to the list of children of the parent. history_list contains all the nodes leading
        # to the current node, parent node will use the last element of the list history_list[-1]
        # to index its dictionary of children
        self.parent.append_child(self, history_list)
        # actions contains a list of action split by spaces
        self.actions = actions.split()
        # player stores the player that plays the current node
        self.player = player
        self.level = self.parent.level + 1
        return self

    def compute_strategies_to_terminal_nodes(self):
        strategies_list = []
        for child in self.children.values():
            strategies_list.extend(child.compute_strategies_to_terminal_nodes())
        return strategies_list

    def compute_payoff_coordinate_vector(self, player, strategies_list, difference_of_number_of_nodes):
        # vector used to define the coordinates of the node in the payoff space, each dimension contains an outcome of
        # the player of the interested payoff space
        payoff_vector = []
        # iterate over the sequence of strategies describing the order of actions we have to follow
        for strategy in strategies_list:
            # add the payoff of the desired child to the payoff vector.
            # [strategy[1:]] builds a list and eats up the first element of the strategy to move on to the second step
            # of the strategy
            payoff_vector.extend(self.children[strategy[0]]
                                 .compute_payoff_coordinate_vector(player,
                                                                   [strategy[1:]],
                                                                   difference_of_number_of_nodes))
        return payoff_vector
