# class PokerGame:
#     def __init__(self):
#         self.players = []
#         self.deck = []
#         self.tree = None
#         self.infoStructure = None
#         self.actions = []
#
#
# class Card:
#     def __init__(self):
#         self.cardName = None
#         self.value = None
#
#     def getValue(self):
#
#
# class Action:
#     def __init__(self):
#         self.name = None
#         self.probability = None
#
#
# class InfoStructure:  # list of information sets of player1 and player2
#     def __init__(self):
#         self.infoSets1 = []
#         self.infoSets2 = []
#
#
# class InfoSet:  # list of nodes for each information set
#     def __init__(self):
#         self.infoNodes = []


class Node:
    def __init__(self):
        self.history = []
        self.children = {}
        self.actions = []
        self.infoset = []
        self.signals = {}
        self.parent = None
        self.cards = []
        self.payoffs = {}

    def node_finder(self, history):
        if len(history) == 1:
            return self
        else:
            for i in self.children.values():
                if i.history[-1] == history[0]:
                    return i.node_finder(i, history[1:])
            return None

    def appendChild(self, node):
        self.children(node)

    def createRootNode(self, actions):
        self.history = []
        values = actions.split()
        for i in values :
            splitted_signals = i.split('=')
            #self.children[splitted_values[0]] = Node('C:'+ splitted_values[0])
            #self.children[splitted_values[0]].setCards(splitted_values[1])
            self.signals[splitted_signals[0]] = float(splitted_signals[1])
            self.actions.append(splitted_signals[1])
        sum = 0
        for j in self.signals :
            sum += self.signals[j]
        for k in self.signals :
            self.signals[k] = self.signals[j]/sum
        return self

    def createActionNode(self, history, player, actions, root):
        history_splitted = history.split('/')
        self.history = history_splitted
        self.parent = root.node_finder(history_splitted[1:])
        self.parent.appendChild(self)
        actions_splitted = actions.split()
        for i in actions_splitted :
            self.actions.append(actions_splitted[i])
        self.cards = self.parent.getCards()
        return self

    def createChanceNode(self, history, actions, root):
        history_splitted = history.split('/')
        self.history = history_splitted
        self.parent = root.node_finder(history_splitted[1:])
        self.parent.appendChild(self)
        actions_list = actions.split()
        for i in actions_list:
            splitted_action = i.split('=')
            #self.children[splitted_values[0]] = Node()
            #self.children[splitted_values[0]].setCards(splitted_values[1])
            self.signals[splitted_action[0]] = splitted_action[1]
            self.actions.append(splitted_action[1])
        sum = 0
        for j in self.signals:
            sum += self.signals[j]
        for k in self.signals:
            self.signals[k] = self.signals[k] / sum
        return self

    def createLeafNode(self, history, payoffs, root):
        history_splitted = history.split('/')
        self.history = history_splitted
        self.parent = root.node_finder(history_splitted[1:])
        self.parent.appendChild(self)
        payoffs_list = payoffs.split()
        for i in payoffs_list:
            splitted_payoffs = i.split('=')
            self.payoffs[splitted_payoffs[0]]=splitted_payoffs[1]
        return self
    def appendCards(self, cards):
        self.cards.append(cards)

    def getCards(self):
        return self.cards


    def setCards(self, cards):
        self.cards = cards

    # def nextNode(action):
    #
    # def getParent():
    #
    # def getActions():
    #
    # def getPlayer():
    #
    # def getUtility():
    #
    # def getCurrentNode():
    #
    # def setNextNode(self, action):
    #
    # def setParent(Tree):
    #
    # def setActions():
