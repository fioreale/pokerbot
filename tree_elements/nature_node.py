import copy

import numpy as np

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
        self.level = 0
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
        support_sum = 0  # support variable used to compute the normalized probabilities
        # cycle through the dictionary of signals
        for j in self.signals:
            support_sum += self.signals[j]  # compute the sum of all non-normalized probability values
        # cycle through the dictionary of signals
        for k in self.signals:
            # overwrite each non-normalized probability with its normalized value
            if support_sum != 0:
                self.signals[k] = float(self.signals[k] / support_sum)
            else:
                self.signals[k] = 0.0
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
        total_sum_support = 0  # support variable used to compute the normalized probabilities
        # cycle through the dictionary of signals
        for j in self.signals:
            total_sum_support += self.signals[j]  # compute the sum of all non-normalized probability values
        # cycle through the dictionary of signals
        for k in self.signals:
            # overwrite each non-normalized probability with its normalized value
            self.signals[k] = self.signals[k] / total_sum_support
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
            if strategy[0].split(':')[1] not in self.actions:
                payoff_vector = [0 for i in range(difference_of_number_of_nodes)]
            else:
                payoff_vector.extend(self.children[strategy[0]].
                                     compute_payoff_coordinate_vector(player,
                                                                      [strategy[1:]],
                                                                      difference_of_number_of_nodes))
        return payoff_vector

    def compute_payoffs_from_node(self):
        payoffs_vector = []
        for action in sorted(self.actions):
            payoffs_vector.extend(self.children['C:' + action].compute_payoffs_from_node())
        return payoffs_vector

    def change_payoffs(self, payoffs_vector):
        assigned_terminal_nodes = 0
        for action in sorted(self.actions):
            n_of_terminal_nodes = self.children['C:' + action] \
                .compute_number_of_terminal_nodes()
            self.children['C:' + action] \
                .change_payoffs(payoffs_vector[assigned_terminal_nodes:n_of_terminal_nodes + assigned_terminal_nodes])
            assigned_terminal_nodes += n_of_terminal_nodes

    def create_new_tree(self, subgame, probabilities_to_subgame):
        actions_string = ''
        actions_index = 0
        for infoset in subgame:
            for node in infoset.info_nodes.values():
                actions_string += str(actions_index) + '=' \
                                  + str(probabilities_to_subgame['/' + '/'.join(node.history)]) + ' '
                actions_index += 1
        root = self.create_root_node(actions_string[:-1])

        actions_index = 0
        for infoset in subgame:
            for node in infoset.info_nodes.values():
                root.children['C:' + str(actions_index)] = node
                root.strategies_probabilities.append(probabilities_to_subgame['/' + '/'.join(node.history)])
                root.signals[str(actions_index)] = probabilities_to_subgame['/' + '/'.join(node.history)]
                actions_index += 1
        return root

    def get_infosets_of_tree(self):
        infosets = []
        for child in self.children.values():
            child_infosets = child.get_infosets_of_tree()
            if child_infosets is not None:
                infosets = list(set(infosets + child_infosets))
        return infosets

    def play(self):
        random_number = np.random.choice(len(self.actions), p=list(self.signals.values()))
        sampled_action = self.actions[random_number]
        child = self.children['C:' + sampled_action]
        return child.play()
