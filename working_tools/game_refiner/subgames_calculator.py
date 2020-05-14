from tree_elements.action_node import ActionNode
from working_tools.abstraction_generator.infosets_navigator import get_infosets_of_tree_level


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
            probabilities_dict[''.join(node.history)] = recursive_compute_probabilities(node)
    return probabilities_dict


def recursive_compute_probabilities(node):
    if node.parent is None:
        return 1
    else:
        node_action = node.history[-1].split(':')[-1]
        strategy_index = node.parent.actions.index(node_action)
        return node.parent.strategies_probabilities[strategy_index] * recursive_compute_probabilities(node.parent)
