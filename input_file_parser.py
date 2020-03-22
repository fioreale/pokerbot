import os
import re
import utilities

from tree_elements.infoSet import InfoSet
from tree_elements.nature_node import NatureNode
from tree_elements.action_node import ActionNode
from tree_elements.terminal_node import TerminalNode
from tree_elements.infoStructure import InfoStructure

rx_dict = {                                             # regex to identify
    'root_node': re.compile(r'node / chance actions (?P<actions>.*)'),
    'action_node': re.compile(r'node (?P<history>.*?) player (?P<player>[1|2]) actions (?P<actions>.*)'),
    'chance_node': re.compile(r'node (?P<history>.*?) chance actions (?P<actions>.*)'),
    'leaf_node': re.compile(r'node (?P<history>.*?) leaf payoffs (?P<payoffs>.*)'),
    'infoset': re.compile(r'infoset (?P<history>.*?) nodes (?P<nodes>.*)')
}


def parse_line(line):                                   # match regex in the line
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


def parse_file(filepath):
    with open(filepath, 'r') as file_object:
        lines = file_object.readlines()
        ordered_lines = sorted(lines)                   # sorting lines
        root = NatureNode()
        for line in ordered_lines:                      # at each line check for a match with a regex
            key, match = parse_line(line)

            if key == 'root_node':
                actions = match.group('actions')
                root.createRootNode(actions)

            if key == 'action_node':
                history = match.group('history')
                actions = match.group('actions')
                player = match.group('player')
                action_node = ActionNode()
                action_node.createActionNode(history, player, actions, root)

            if key == 'chance_node':
                history = match.group('history')
                # actions contains all the actions after the keyword 'action'
                actions = match.group('actions')
                chance_node = NatureNode()
                chance_node.createChanceNode(history, actions, root)

            if key == 'leaf_node':
                history = match.group('history')
                actions = match.group('payoffs')
                leaf_node = TerminalNode()
                leaf_node.createTerminalNode(history, actions, root)
    return root

def parse_infoset(filepath, tree):
    with open(filepath, 'r') as file_object:
        lines = file_object.readlines()
        ordered_lines = sorted(lines)
        infoStructure = InfoStructure()
        for line in ordered_lines:
            key, match = parse_line(line)
            if key == 'infoset':
                history = match.group('history')
                nodes = match.group('nodes')
                newInfoSet = InfoSet()
                newInfoSet.createInfoSet(history, nodes, tree)
                infoStructure.assignInfoSet(newInfoSet)
    return infoStructure


if __name__ == '__main__':
    tree = parse_file(os.path.join(os.getcwd(), 'inputs', 'kuhn.txt'))
    infoSets = parse_infoset(os.path.join(os.getcwd(), 'inputs', 'kuhn.txt'), tree)
    utilities.visualize(tree, 0)
    cluster_table = utilities.clustering_table_creation(tree)
    utilities.print_cluster_table(tree)
