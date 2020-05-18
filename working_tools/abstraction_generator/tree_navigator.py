import operator
from datetime import datetime
import sys
from pathlib import Path


def get_tree_level(root, level):
    if level == 0:
        return [root]

    node_collection = []
    if level > 1:
        for child in root.children.values():
            # node_collection.append(get_tree_level(child, level - 1))
            node_collection += get_tree_level(child, level - 1)
        return node_collection
    else:
        for node in root.children.values():
            node_collection += [node]
        return node_collection


def split_node_list(node_list):
    set_of_actions = list()
    sets_of_nodes = list()
    for node in node_list:
        if node.actions not in set_of_actions:
            set_of_actions.append(node.actions)
            sets_of_nodes.append(list())
    for node in node_list:
        sets_of_nodes[set_of_actions.index(node.actions)].append(node)
    return sets_of_nodes


def find_tree_height(node, level):
    max_height = level
    if node.children is not None:
        for child in node.children.values():
            found_height = find_tree_height(child, level + 1)
            if max_height < found_height:
                max_height = found_height
    return max_height


def file_strategies_saver(tree):
    Path("text_files/outputs").mkdir(parents=True, exist_ok=True)
    original = sys.stdout
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d__%H_%M_%S")
    sys.stdout = open('text_files/outputs/strategies_' + current_time + '.txt', 'w')
    infoset_list = tree.get_infosets_of_tree()
    for infoset in sorted(infoset_list, key=operator.attrgetter('name')):
        node = list(infoset.info_nodes.values())[0]
        print('infoset ' + infoset.name + ' strategies', end=' ')
        index = 0
        for action in node.actions:
            if index == len(node.actions)-1:
                print(action + '=' + str(node.strategies_probabilities[index]), end='')
            else:
                print(action + '=' + str(node.strategies_probabilities[index]), end=' ')
            index += 1
        print()
    sys.stdout = original
