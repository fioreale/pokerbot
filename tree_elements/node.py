import numpy as np

from working_tools.abstraction_generator import infoset_numbers_calculator


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
    def compute_payoff_coordinate_vector(self, player, strategies_list, difference_of_number_of_nodes):
        return

    # abstract
    def compute_number_of_terminal_nodes(self):
        number_of_nodes = 0
        for child in self.children.values():
            number_of_nodes += child.compute_number_of_terminal_nodes()
        return number_of_nodes

    def compress_tree(self, kmeans, strategies_list_dictionary, nodes_letter_list_dict):

        for history_group_key, history_group_couple in kmeans.items():

            infoset_ordered_list = history_group_couple[0]
            kmeans_results = history_group_couple[1]

            for kmeans_label in set(kmeans_results.labels_):

                same_label_infosets_indexes = np.argwhere(kmeans_results.labels_ == kmeans_label)
                # group all infosets with same labels
                same_label_infosets_ndarray = np.array(infoset_ordered_list)[same_label_infosets_indexes].flatten()
                same_label_infosets_list = same_label_infosets_ndarray.tolist()

                max_number_of_terminal_nodes, max_num_of_nodes = infoset_numbers_calculator.\
                    max_numbers_calculator(same_label_infosets_list)
                max_num_of_nodes_infoset = infoset_numbers_calculator.\
                    max_nodes_infoset_finder(same_label_infosets_list,
                                             max_num_of_nodes)

                if list(max_num_of_nodes_infoset.info_nodes.values())[0].player == '1':
                    player = '2'
                else:
                    player = '1'

                # vector used to store the payoffs of the different different from the one on which we have computed
                # the payoff space
                different_player_payoff_vector = []

                for infoset in same_label_infosets_list:
                    difference_of_terminal_nodes = max_number_of_terminal_nodes - infoset.\
                        compute_number_of_terminal_nodes()

                    different_player_payoff_vector.\
                        append(infoset.compute_payoff_of_other_player(player,
                                                                      strategies_list_dictionary[history_group_key],
                                                                      difference_of_terminal_nodes,
                                                                      nodes_letter_list_dict[history_group_key]))

                different_player_payoff_vector = np.mean(np.array(different_player_payoff_vector), axis=0)
                
                if list(max_num_of_nodes_infoset.info_nodes.values())[0].player == '1':
                    both_players_payoff_vector = np.array(
                        [kmeans_results.cluster_centers_[kmeans_label], different_player_payoff_vector]).T
                else:
                    both_players_payoff_vector = np.array(
                        [different_player_payoff_vector, kmeans_results.cluster_centers_[kmeans_label]]).T

                both_players_payoff_vector = both_players_payoff_vector.tolist()

                max_num_of_nodes_infoset.apply_new_payoff(strategies_list_dictionary[history_group_key],
                                                          nodes_letter_list_dict[history_group_key],
                                                          both_players_payoff_vector)

                filtered_list = filter(lambda x: x != max_num_of_nodes_infoset, same_label_infosets_list)

                for infoset in filtered_list:
                    for node in infoset.info_nodes.values():
                        node.parent.children.pop(node.history[-1])

    def change_payoff(self, both_players_payoff_vector, strategies_list):
        num_of_assigned_terminal_nodes = 0
        for strategy in strategies_list:
            # number_of_terminal_nodes = self.children[strategy[0]].compute_number_of_terminal_nodes()
            if not(strategy[0].split(':')[1] not in self.actions):
                self.children[strategy[0]].\
                    change_payoff(both_players_payoff_vector[num_of_assigned_terminal_nodes:
                                                             num_of_assigned_terminal_nodes + 1],
                                  [strategy[1:]])
                num_of_assigned_terminal_nodes += 1
