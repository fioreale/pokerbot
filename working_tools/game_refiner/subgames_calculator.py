import copy
from tree_elements.action_node import ActionNode
from tree_elements.terminal_node import TerminalNode
from working_tools.abstraction_generator.infosets_navigator import get_infosets_of_tree_level
import numpy as np


def subgame_calculator(tree, level):
    # retrieves  all the infosets of the level
    infosets_of_the_level = get_infosets_of_tree_level(tree, level)

    subgames_list = []

    for infoset in infosets_of_the_level:
        if not any(infoset in subgame_infoset for subgame_infoset in subgames_list):
            subgame_infosets = [infoset]
            for node in infoset.info_nodes.values():
                for child in node.children.values():
                    if isinstance(child, ActionNode):
                        for node_infoset_sibling in child.infoset.info_nodes.values():
                            if node_infoset_sibling.parent.infoset not in subgame_infosets:
                                subgame_infosets.append(node_infoset_sibling.parent.infoset)
            subgames_list.append(subgame_infosets)

    return subgames_list


def compute_probabilities_to_subgame(subgame):
    probabilities_dict = {}
    for infoset in subgame:
        for node in infoset.info_nodes.values():
            probabilities_dict['/' + '/'.join(node.history)] = recursive_compute_probabilities(node)
    return probabilities_dict


def recursive_compute_probabilities(node):
    if node.parent is None:
        return 1
    else:
        parent = node.parent
        node_action = node.history[-1].split(':')[-1]
        if isinstance(parent, ActionNode):
            strategy_index = node.parent.actions.index(node_action)
            return node.parent.strategies_probabilities[strategy_index] * recursive_compute_probabilities(node.parent)
        else:
            return node.parent.signals[node_action] * recursive_compute_probabilities(node.parent)


def compress_subgame(subgame):
    current_player = int(list(subgame[0].info_nodes.values())[0].player) - 1
    for infoset in subgame:
        for node in infoset.info_nodes.values():
            for child in node.children.values():
                recursive_compression(child, current_player)


def recursive_compression(node, current_player):
    # for every child which is a TerminalNode we store its payoffs

    if not isinstance(node, TerminalNode):
        for child in node.children.values():
            recursive_compression(child, current_player)

        if isinstance(node, ActionNode):
            if int(node.player) - 1 == current_player:
                payoffs_of_children = []
                for child in node.children.values():
                    payoffs_of_children.append(child.compute_payoffs_from_node())
                max_payoff_length = find_max_payoff_length(payoffs_of_children)
                payoffs_of_children = list(map(lambda x: extend_to_max_length(x, max_payoff_length), payoffs_of_children))
                payoffs_of_children = np.array(payoffs_of_children)
                weights = np.array(node.strategies_probabilities, dtype='float')
                payoffs_weighted_average = np.average(a=payoffs_of_children, axis=0, weights=weights)
                list_of_children = list(node.children.values())
                best_child = find_max_action_child(list_of_children)
                best_child.change_payoffs(payoffs_weighted_average)
                for child in list_of_children:
                    if child != best_child and isinstance(child, ActionNode):
                        child.infoset.info_nodes.pop('/' + '/'.join(child.history))
                node.parent.children[node.history[-1]] = best_child


def find_max_payoff_length(list_of_payoffs):
    max_length = 0
    for payoff_vector in list_of_payoffs:
        payoff_vector_length = len(payoff_vector)
        if payoff_vector_length > max_length:
            max_length = payoff_vector_length
    return max_length


def extend_to_max_length(payoff_vector, max_length):
    index = 0
    new_payoff_vector = copy.deepcopy(payoff_vector)
    while len(new_payoff_vector) < max_length:
        new_payoff_vector.append(payoff_vector[index])
        index += 1
        if index > len(payoff_vector) - 1:
            index = 0
    return new_payoff_vector


def find_max_action_child(list_of_children):
    max_action_child = None
    max_terminal_nodes_number = 0
    for child in list_of_children:
        node_terminal_nodes_number = child.compute_number_of_terminal_nodes()
        if node_terminal_nodes_number > max_terminal_nodes_number:
            max_terminal_nodes_number = node_terminal_nodes_number
            max_action_child = child
    return max_action_child
