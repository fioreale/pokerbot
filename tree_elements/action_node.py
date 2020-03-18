from tree_elements.node import Node


class ActionNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.player = None

    def getActions(self):
        return self.actions

    def createActionNode(self, history, player, actions, root):
        history_list = history.split('/')[1:]                           # deleted first empty element of the history
        self.history = history_list
        self.parent = root.node_finder(history_list[:-1])               # called node finder without last element (ASK LUCIANO!) ---> In fact Luciano is right!
        self.parent.appendChild(self, history_list)
        self.actions = actions.split()
        self.player = int(player)
        self.cards = self.parent.getCards()
        return self
