from tree_elements.node import Node


class NatureNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.signals = {}
        self.player = 'C'

    def createRootNode(self, actions):
        self.history = []
        actions = actions.split()
        for i in actions:
            splitted_signals = i.split('=')
            self.signals[str(splitted_signals[0])] = float(splitted_signals[1])
            self.actions.append(splitted_signals[1])
        sum = 0
        for j in self.signals:
            sum += self.signals[j]
        for k in self.signals:                                              # normalization of the signals
            self.signals[k] = self.signals[k] / sum
        return self

    def createChanceNode(self, history, actions, root):                     # TODO these actions are not actions of the player
        history_list = history.split('/')[1:]                               # deleted first empty element of the history
        self.history = history_list
        self.parent = root.node_finder(history_list[:-1])                   # called node finder without last element (ASK LUCIANO!)
        self.parent.appendChild(self, history_list)
        actions_list = actions.split()
        for i in actions_list:
            splitted_action = i.split('=')
            self.signals[splitted_action[0]] = float(splitted_action[1])
            self.actions.append(splitted_action[1])
        sum = 0
        for j in self.signals:
            sum += self.signals[j]
        for k in self.signals:                                              # normalization of the signals
            self.signals[k] = self.signals[k] / sum
        return self

