from tree_elements.node import Node


class ActionNode(Node):
    def __init__(self):
        Node.__init__(self)

    # def getActions():
    #
    # def setActions():

    def createActionNode(self, history, player, actions, root):
        history_list = history.split('/')[1:]
        self.history = history_list
        self.parent = root.node_finder(history_list[:-1])
        self.parent.appendChild(self, history_list)
        self.actions = actions.split()
        self.cards = self.parent.getCards()
        return self
