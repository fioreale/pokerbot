import utilities


class Node:
    def __init__(self):         # class initializator
        self.history = []
        self.children = {}
        self.actions = []
        self.parent = None
        self.cards = []

    def node_finder(self, history):     # recursive function that traverse the history and returns its last node
        if len(history) == 0:
            return self
        else:
            return self.children[history[0]].node_finder(history[1:])

    def appendChild(self, node, history):
        self.children[history[-1]] = node

    def appendCards(self, cards):
        if len(self.cards) > 1:
            self.cards.append(utilities.in_chars(cards[0]))
        else:
            return ValueError("No cards in the player hand")

    def getCards(self):
        return self.cards

    def setCards(self, cards):
        self.cards = cards

    def print_tree(self, level):
        l = 0
        while (l < level):
            print('    ', end = '')
            l += 1
        if len(self.history) > 0:
            print(self.history[-1])
        else:
            print('C')
        for i in self.children.values():
            i.print_tree(level + 1)
