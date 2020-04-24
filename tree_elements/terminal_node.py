from tree_elements.node import Node

# class used to build terminal nodes which store the payoff value for the players
# extends superclass Node


class TerminalNode(Node):

    # constructor method. Initializes the list of payoffs as [None, None]
    def __init__(self):
        Node.__init__(self)
        self.payoffs = [None, None]

    # initialization method of the class where we set up the attributes values
    # history contains the path of nodes that leads to the node to be created
    # Example: '/C:99/P1:raise2/P2:raise2/P1:c'
    # payoff contains the list of outcomes for each player. Example: '1=0.000000 2=0.000000'
    # root contains the root node of the game tree
    def create_terminal_node(self, history, payoffs, root):
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
        # payoffs_list contains the list of payoffs split by spaces
        payoffs_list = payoffs.split()
        for payoff in payoffs_list:
            # each payoff is split in player identifier and outcome value
            payoff_split_values_list = payoff.split('=')
            # payoff_player_identifier contains the identifier of the player
            payoff_player_identifier = payoff_split_values_list[0]
            # payoff_player_outcome contains the outcome value
            payoff_player_outcome = float(payoff_split_values_list[1])
            # based on the player identifier we store the outcome value in the payoff list
            if payoff_player_identifier == '1':
                self.payoffs[0] = payoff_player_outcome
            else:
                self.payoffs[1] = payoff_player_outcome
        return self

    # override function that returns the payoff list
    def compute_utilities(self):
        return self.payoffs

    def compute_metric(self, player):
        values = self.compute_hands_values(player)
        metric = values[0] - values[1] + values[2] / 2
        return metric

    def compute_hands_values(self, player):
        if player == '1':
            if self.payoffs[0] > self.payoffs[1]:
                return 1, 0, 0
            elif self.payoffs[0] < self.payoffs[1]:
                return 0, 1, 0
            else:
                return 0, 0, 1

        else:
            if self.payoffs[1] > self.payoffs[0]:
                return 1, 0, 0
            elif self.payoffs[1] < self.payoffs[0]:
                return 0, 1, 0
            else:
                return 0, 0, 1
