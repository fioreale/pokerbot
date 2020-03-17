import os
import re


from tree_elements.nature_node import NatureNode
from tree_elements.action_node import ActionNode
from tree_elements.terminal_node import TerminalNode

rx_dict = {
    'root_node': re.compile(r'node / chance actions (?P<actions>.*)'),
    'action_node': re.compile(r'node (?P<history>.*?) player (?P<player>[1|2]) actions (?P<actions>.*)'),
    'chance_node': re.compile(r'node (?P<history>.*?) chance actions (?P<actions>.*)'),
    'leaf_node': re.compile(r'node (?P<history>.*?) leaf payoffs (?P<payoffs>.*)'),
    'infoset': re.compile(r'infoset (?P<history>.*?) nodes (?P<nodes>.*)')
}


def parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """

    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None


def parse_file(filepath):
    """
    Parse text at given filepath

    Parameters
    ----------
    filepath : str
        Filepath for file_object to be parsed

    Returns
    -------
    data : pd.DataFrame
        Parsed data

    """

    data = []  # create an empty list to collect the data
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        lines = file_object.readlines()
        ordered_lines = sorted(lines)
        root = NatureNode()
        for line in ordered_lines:
            # at each line check for a match with a regex
            key, match = parse_line(line)
            # extract school name
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
                actions = match.group('actions')
                chance_node = NatureNode()
                chance_node.createChanceNode(history, actions, root)

            if key == 'leaf_node':
                history = match.group('history')
                actions = match.group('payoffs')
                leaf_node = TerminalNode()
                leaf_node.createTerminalNode(history, actions, root)

            # if key == 'infoset':
            #     history = match.group('history')
            #     arguments = match.group('arguments')
    return root


if __name__ == '__main__':
    tree = parse_file(os.path.join(os.getcwd(), 'inputs', 'leduc3.txt'))
    tree.print_tree(0)
