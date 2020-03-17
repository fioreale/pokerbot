from tree_elements.node import Node


class NatureNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.signals = {}

    def createRootNode(self, actions):
        self.history = []
        actions = actions.split()
        for i in actions:
            splitted_signals = i.split('=')
            # self.children[splitted_values[0]] = Node('C:'+ splitted_values[0])
            # self.children[splitted_values[0]].setCards(splitted_values[1])
            self.signals[str(splitted_signals[0])] = float(splitted_signals[1])
            self.actions.append(splitted_signals[1])
        sum = 0
        for j in self.signals:
            sum += self.signals[j]
        for k in self.signals:
            self.signals[k] = self.signals[k] / sum
        return self

    def createChanceNode(self, history, actions, root):
        history_list = history.split('/')[1:]
        self.history = history_list
        self.parent = root.node_finder(history_list[:-1])
        self.parent.appendChild(self, history_list)
        actions_list = actions.split()
        for i in actions_list:
            splitted_action = i.split('=')
            # self.children[splitted_values[0]] = Node()
            # self.children[splitted_values[0]].setCards(splitted_values[1])
            self.signals[splitted_action[0]] = float(splitted_action[1])
            self.actions.append(splitted_action[1])
        sum = 0
        for j in self.signals:
            sum += self.signals[j]
        for k in self.signals:
            self.signals[k] = self.signals[k] / sum
        return self