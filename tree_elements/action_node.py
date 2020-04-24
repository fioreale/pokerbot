from tree_elements.nature_node import NatureNode
from tree_elements.node import Node


# class used to build nodes where players chose which action to play
# extends superclass Node


class ActionNode(Node):
    def __init__(self):
        Node.__init__(self)

    # initialization method of the class where we set up the attributes values
    # history contains the path of nodes that leads to the node to be created
    # Example: '/C:99/P1:raise2/P2:raise2/P1:c'
    # player contains the number of the player. Example: '1'
    # actions contains a list of actions available for the player of the node. Example: 'c f'
    # root is the root node of the tree
    def create_action_node(self, history, player, actions, root):
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
        self.actions = actions.split()
        # player stores the player that plays the current node
        self.player = player
        return self

    def compute_metric(self, player, action):
        # if the action value is not already set
        if self.action_value is None:
            # compute the node values
            values = self.compute_action_value(player, action)

            # calculate the metric
            # METRIC, FIRST PROPOSITION = wins - losses + draws/2
            # metric = (values[0] - values[1] + values[2] / 2)
            # METRIC, SECOND PROPOSITION = (wins - losses + draws/2) / cardinality(infoset)
            # metric = (values[0] - values[1] + values[2] / 2) / len(self.infoset.info_nodes.values())
            # METRIC, THIRD PROPOSITION = (WINS POINTS(positives) + LOSSES POINTS(negatives) + DRAWS(zeros)
            metric = (values[0] + values[1] + values[2])

            # CHECKED: always true
            # if self.infoset is not None:
            for node in self.parent.infoset.info_nodes.values():
                child = node.children['P' + node.player + ':' + action]
                child.action_value = metric
            # CHECKED: never called
            # else:
            #     self.action_value = metric
            self.action_value = metric
        return self.action_value

    def compute_action_value(self, player, input_action):
        # initialize metric parameters
        wins = 0
        losses = 0
        draws = 0
        # if the action value is not already set
        if self.action_value is None:
            # TODO verify the correctness of the operations done under this condition
            if type(self.parent) is NatureNode:
                for action in self.actions:
                    values = self.children['P' + self.player + ':' + action].compute_action_value(player, action)
                    wins += values[0]
                    losses += values[1]
                    draws += values[2]

            # CHECKED: always true
            # elif self.infoset is not None:

            else:
                # for each node belonging to the infoset of the parent
                for node in self.parent.infoset.info_nodes.values():
                    # select the child corresponding to the same action that lead to the current node
                    child = node.children['P' + node.player + ':' + input_action]
                    # for each action of the child node
                    for action in child.actions:
                        # call compute action value
                        values = child.children['P' + child.player + ':' + action].compute_action_value(player, action)
                        # update values of the wins, losses and draws
                        wins += values[0]
                        losses += values[1]
                        draws += values[2]

            # CHECKED: never called
            # else:
            #     for node in self.parent.infoset.info_nodes.values():
            #         child = node.children['P' + node.player + ':' + input_action]
            #         for action in child.actions:
            #             values = child.children['P' + child.player + ':'+ action].compute_hands_values(player, action)
            #             wins += values[0]
            #             losses += values[1]
            #             draws += values[2]

        # return values
        return wins, losses, draws
