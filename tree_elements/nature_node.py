from tree_elements.node import Node

# class used to represent the chance nodes in the tree


class NatureNode(Node):
    def __init__(self):
        Node.__init__(self)
        # signals is a dictionary indexed by name of the possible action and stores the value of the probability
        # of that action to be chosen.
        # Example: {['JK' : 0.2000; ... ]}
        self.signals = {}
        # the player of this nodes is always the chance player
        self.player = 'C'

    # function to set up the values of the root node
    # actions contains the list of possible actions with their corresponding probabilities.
    # Example: '99=2.000000 9T=4.000000 9J=4.000000 9Q=4.000000 ... '
    def create_root_node(self, actions):
        # history is initialized as an empty list as there are no nodes that leads to the root node
        self.history = []
        # the list of actions is split by spaces
        actions = actions.split()
        for action in actions:
            # each action is split in name and non-normalized probability value
            split_signals = action.split('=')
            # signal_action_name contains the name of action
            signal_action_name = str(split_signals[0])
            # signal_action_value contains the non-normalized probability value
            signal_action_value = float(split_signals[1])
            # the non-normalized probability value is saved in the dictionary indexed by the action name
            self.signals[signal_action_name] = signal_action_value
            # the action name is saved in the list of actions available for the current node
            self.actions.append(signal_action_name)
        support_sum = 0         # support variable used to compute the normalized probabilities
        # cycle through the dictionary of signals
        for j in self.signals:
            support_sum += self.signals[j]      # compute the sum of all non-normalized probability values
        # cycle through the dictionary of signals
        for k in self.signals:
            # overwrite each non-normalized probability with its normalized value
            self.signals[k] = float(self.signals[k] / support_sum)
        return self

    # function to set up the values of the chance nodes in the middle of the tree
    # history contains the path of nodes that leads to the node to be created
    # Example: '/C:99/P1:raise2/P2:raise2/P1:c'
    def create_chance_node(self, history, actions, root):
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
        actions_list = actions.split()
        for action in actions_list:
            # each action is split in name and non-normalized probability value
            split_action = action.split('=')
            # signal_action_name contains the name of action
            chance_action_name = split_action[0]
            # signal_action_value contains the non-normalized probability value
            chance_action_value = float(split_action[1])
            # the non-normalized probability value is saved in the dictionary indexed by the action name
            self.signals[chance_action_name] = chance_action_value
            # the action name is saved in the list of actions available for the current node
            self.actions.append(str(chance_action_name))
        total_sum_support = 0       # support variable used to compute the normalized probabilities
        # cycle through the dictionary of signals
        for j in self.signals:
            total_sum_support += self.signals[j]        # compute the sum of all non-normalized probability values
        # cycle through the dictionary of signals
        for k in self.signals:
            # overwrite each non-normalized probability with its normalized value
            self.signals[k] = self.signals[k] / total_sum_support
        return self

    def compute_utilities(self):
        max_utility = [0.0, 0.0]
        # cycle through each action to retrieve the child node utilities
        # returned utilities are a list [utility_player_1, utility_player_2]
        for action in self.actions:
            self.utilities[action] = self.children[self.player + ':' + action].compute_utilities()
        # initialization of the list max_utility where  we're gonna save the average utility for this node
        max_utility = [0.0, 0.0]
        for signal_action in self.actions:
            weighted_utility_first_player = self.utilities[signal_action][0] * self.signals[signal_action]
            weighted_utility_second_player = self.utilities[signal_action][1] * self.signals[signal_action]
            max_utility[0] += weighted_utility_first_player
            max_utility[1] += weighted_utility_second_player
        return max_utility

    def compute_hands_values(self, player):
        wins = 0
        loses = 0
        draws = 0
        if self.hand_value is None:
            if self.infoset is not None:
                for node in self.infoset.info_nodes.values():
                    for action in node.actions:
                        values = self.children['C:' + action].compute_hands_values(player)
                        wins += values[0]
                        loses += values[1]
                        draws += values[2]
            else:
                for action in self.actions:
                    values = self.children['C:' + action].compute_hands_values(player)
                    wins += values[0]
                    loses += values[1]
                    draws += values[2]
        return wins, loses, draws

