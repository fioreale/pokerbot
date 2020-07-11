import re

from game_model.info_set import InfoSet
from game_model.nature_node import NatureNode
from game_model.action_node import ActionNode
from game_model.terminal_node import TerminalNode
from game_model.info_structure import InfoStructure

rx_dict = {
    # regex to identify root node
    # example in 'input - kuhn.txt': node / chance actions JQ=1.000000 JK=1.000000 QJ=1.000000 QK=1.000000 ...
    # example in 'input - leduc_5.txt': node / chance actions 99=2.000000 9T=4.000000 9J=4.000000 9Q=4.000000 ...
    # ?P<actions> matches after the keyword actions. Example: '99=2.000000 9T=4.000000 9J=4.000000 9Q=4.000000'
    'root_node': re.compile(r'node / chance actions (?P<actions>.*)'),

    # regex to identify any action node
    # example in 'input - kuhn.txt': node /C:JK/P1:c/P2:r player 1 actions c f
    # example in 'input - leduc_5.txt': node /C:KK/P1:c/P2:c/C:Q/P1:c player 2 actions raise4 c
    # ?P<history> matches the list of nodes that leads to the current nodes including itself after keyword node
    # Example: '/C:KK/P1:c/P2:c/C:Q/P1:c'
    # ?P<player> matches only the number of player after keyword player. Example: '1'
    # ?P<actions> matches after the keyword actions. Example: 'c f'
    'action_node': re.compile(r'node (?P<history>.*?) player (?P<player>[1|2]) actions (?P<actions>.*)'),

    # regex to identify a chance node in the middle of the game
    # example in 'input - kuhn.txt': no examples
    # example in 'input - leduc_5.txt': node /C:99/P1:raise2/P2:raise2/P1:c chance actions T=2.000000 J=2.000000 ...
    # ?P<history> matches the list of nodes that leads to the current nodes including itself after keyword node
    # Example: '/C:99/P1:raise2/P2:raise2/P1:c'
    # ?P<actions> matches after the keyword actions. Example: 'T=2.000000 J=2.000000'
    'chance_node': re.compile(r'node (?P<history>.*?) chance actions (?P<actions>.*)'),

    # regex to identify any leaf node
    # example in 'input - kuhn.txt': node /C:JQ/P1:c/P2:c leaf payoffs 1=-1.000000 2=1.000000
    # example in 'input - leduc_5.txt': node /C:99/P1:raise2/P2:raise2/P1:c/C:K/P1:c/P2:raise4/P1:raise4/P2:c
    # leaf payoffs 1=0.000000 2=0.000000
    # ?P<history> matches the list of nodes that leads to the current nodes including itself after keyword node
    # Example: '/C:99/P1:raise2/P2:raise2/P1:c/C:K/P1:c/P2:raise4/P1:raise4/P2:c'
    # ?P<payoffs> matches the list of payoffs in the terminal node for each player. Example: '1=0.000000 2=0.000000'
    'leaf_node': re.compile(r'node (?P<history>.*?) leaf payoffs (?P<payoffs>.*)'),

    # regex to identify infoset informations
    # example in 'input - kuhn.txt': infoset /C:K?/P1:c/P2:r nodes /C:KJ/P1:c/P2:r /C:KQ/P1:c/P2:r
    # example in 'input - leduc_5.txt': infoset /?9/P1:c/P2:c/C:T/P1:raise4 nodes /C:99/P1:c/P2:c/C:T/P1:raise4
    # /C:T9/P1:c/P2:c/C:T/P1:raise4 /C:J9/P1:c/P2:c/C:T/P1:raise4 ...
    # ?P<history> matches the list of nodes that leads to the current infoset leaving the unknown information
    # unspecified. Example: '/?9/P1:c/P2:c/C:T/P1:raise4'
    # ?P<nodes> matches the list of node indentifiers that belongs to the aforementioned infoset.
    # Example: '/C:99/P1:c/P2:c/C:T/P1:raise4 /C:T9/P1:c/P2:c/C:T/P1:raise4 /C:J9/P1:c/P2:c/C:T/P1:raise4 ...'
    'infoset': re.compile(r'infoset (?P<history>.*?) nodes (?P<nodes>.*)')
}


# function to parse a single line and match the regex inside the line
# input parameters: str line = the line to parse
# returns a couple (str, re.Pattern) corresponding to the dictionary index od the matched regex and the regex object
# def parse_line(line: str) -> (str,  re.Pattern)
# if none string is matched it returns None, None
def parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


# function that parses the entire file and returns the root of the game tree
# def parse_file(filepath: str) -> Node:
# input parameters: str filepath = path of the file to parse
# output: Node root = root node of the game tree
def parse_tree(filepath):
    with open(filepath, 'r') as file_object:
        # reads each line of the file
        lines = file_object.readlines()
        # sorts the lines in alphabetical order
        ordered_lines = sorted(lines)
        # initializes the root node
        root = NatureNode()
        # cycles through each line and parses it
        for line in ordered_lines:
            # regex index and regex object that match the parsed line
            key, match = parse_line(line)

            if key == 'root_node':
                actions = match.group('actions')
                # create the root node with all his parameters
                # actions are passed in the form: '99=2.000000 9T=4.000000 9J=4.000000 9Q=4.000000...'
                root.create_root_node(actions)

            if key == 'action_node':
                history = match.group('history')
                actions = match.group('actions')
                player = match.group('player')
                # create an action node with all his parameters
                # history is passed in the form: '/C:99/P1:raise2/P2:raise2/P1:c'
                # player is passed in the form: '1'
                # actions are passed in the form: 'c f'
                action_node = ActionNode()
                action_node.create_action_node(history, player, actions, root)

            if key == 'chance_node':
                history = match.group('history')
                actions = match.group('actions')
                # create a chance node with all his parameters
                # history is passed in the form: '/C:99/P1:raise2/P2:raise2/P1:c'
                # actions are passed in the form: 'T=2.000000 J=2.000000'
                chance_node = NatureNode()
                chance_node.create_chance_node(history, actions, root)

            if key == 'leaf_node':
                history = match.group('history')
                actions = match.group('payoffs')
                # create a terminal node with all his parameters
                # history is passed in the form: '/C:99/P1:raise2/P2:raise2/P1:c'
                # payoffs are passed in the form: '1=0.000000 2=0.000000'
                leaf_node = TerminalNode()
                leaf_node.create_terminal_node(history, actions, root)
    return root


def parse_infoset(filepath, tree_root):
    with open(filepath, 'r') as file_object:
        # reads each line of the file
        lines = file_object.readlines()
        # sorts the lines in alphabetical order
        ordered_lines = sorted(lines)
        # initializes the InfoStructure object with empty parameters
        info_structure = InfoStructure()
        # cycle through each line od the file
        for line in ordered_lines:
            key, match = parse_line(line)
            if key == 'infoset':
                history = match.group('history')
                nodes = match.group('nodes')
                # create an infoset with all his parameters
                new_info_set = InfoSet()
                # history is passed in the form: '/?9/P1:c/P2:c/C:T/P1:raise4'
                # nodes is passed in the form: '/C:99/P1:c/P2:c/C:T/P1:raise4 /C:T9/P1:c/P2:c/C:T/P1:raise4 ...'
                new_info_set.create_info_set(history, nodes, tree_root)
                # the new infoset is added to the InfoStructure of the tree
                info_structure.assign_info_set(new_info_set, tree_root)
    # return the complete info structure of the game tree
    return info_structure
