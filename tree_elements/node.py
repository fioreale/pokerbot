import utilities


class Node:
    def __init__(self):         # class initializer
        self.history = []
        self.actions = []
        self.children = {}
        self.parent = None
        self.cards = []
        self.infoSet = None
        self.player = None
        self.utilities = {} # utilities dictionary used  to compute backward induction outcomes
        self.utilities_per_action = {} # dictionary where we save all the possible utilities for each single action
                                        # reference Abstraction_Generation.pdf slide 23/67

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

    def compute_utilities(self):
        # cycle through each action to retrieve the child node utilities
        # returned utilities are a list [utility_player_1, utility_player_2]
        for action in self.actions:
            self.utilities[action] = self.children[self.player + ':' + action].compute_utilities()
        # initialization of the list max_utility where  we're gonna save the best utility for this node
        max_utility = self.utilities[self.actions[0]]
        # cycle through the computed utilities to compute the best one
        for utility in self.utilities.items():
            # computation of best utility for first player
            if self.player == '1':
                if utility[0] > max_utility[0]:
                    max_utility = utility
            # computation of best utility for second player
            if self.player == '2':
                if utility[1] > max_utility[1]:
                    max_utility = utility
        # returns best utility which is a vector [utility_player_1, utility_player_2]
        return max_utility
