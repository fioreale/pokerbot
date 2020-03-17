import Utilities

class PokerGame:
    def __init__(self):
        #self.players = []
        self.deck = []
        self.tree = None    # just one Nature Player
        self.infoStructure = None   # list of infosets for each single player
        self.actions = []   # list of possible actions, depending on the type of poker

# class Card:
#     def __init__(self):
#         self.cardName = None
#         self.value = None
#
#     def getValue(self):

class Action:
    def __init__(self):
        self.name = None
        self.probability = None


class InfoStructure:  # list of information sets of player1 and player2
    def __init__(self):
        self.infoSets1 = []
        self.infoSets2 = []


class InfoSet:  # list of nodes for each information set
    def __init__(self):
        self.infoNodes = []


class Node:
    def __init__(self, name):
        self.name=name
        self.children = {}
        #self.infoset = [] maybe it should be referenced a part, and outside the nodes, since an infoset could include nodes of many subtrees
        self.parent = None
        self.cards = []

    def appendCards(self, cards):
        if len(self.cards)>1:
            self.cards.append(Utilities.in_chars(cards[0]))
        else:
            return ValueError("No cards in the player hand")

    def getCards(self):
        return self.cards

    def setCards(self, cards):
        self.cards = Utilities.in_chars(cards)

    def nextNode(action):

    def getParent():

    def getCurrentNode():

    def setNextNode(self, action):

    def setParent(Tree):

    def node_finder(self, history):
        if len(history) == 1:
            return self.children[history[0]]
        else:
            for i in self.children.items():
                if i.name == history[0]:
                    return i.node_finder(i, history[1:])
            return None

class NatureNode(Node):
    def __init__(self,name):
        super.__init__(name)
        self.signals = {}

    def setRoot(self, actions):
        values = actions.split()
        for i in values :
            splitted_values = i.split('=')
            self.children[splitted_values[0]] = Node('C:'+splitted_values[0])
            self.children[splitted_values[0]].setCards(splitted_values[0])
            self.signals[splitted_values[0]] = splitted_values[1]
            self.actions.append(splitted_values[1])
        for j in self.signals :
            sum += self.signals[j]
        for k in self.signals :
            self.signals[k] = self.signals[k]/sum

    def createChanceNode(self, history, actions, root):
        history_splitted = history.split('/')
        self.parent = root.node_finder(history_splitted[1:])
        actions_splitted = actions.split()
        for i in actions_splitted:
            splitted_values = i.split('=')
            self.children[splitted_values[0]] = Node('C:' + splitted_values[0])
            self.children[splitted_values[0]].setCards(splitted_values[1])
            self.signals[splitted_values[0]] = splitted_values[1]
            self.actions.append(splitted_values[1])
        sum = 0
        for j in self.signals:
            sum += self.signals[j]
        for k in self.signals:
            self.signals[k] = self.signals[k] / sum


class ActionNode(Node):
    def __init__(self,name):
        super.__init__(name)
        self.actions = []

    def getActions():

    def setActions():

    def setActionNode(self, history, actions, root):
        history_splitted = history.split('/')
        self.parent = root.node_finder(history_splitted[1:])
        actions_splitted = actions.split()
        for i in actions_splitted :
            self.actions.append(actions_splitted[i])
        self.cards = self.parent.getCards()


class TerminalNode(Node):
    def __init__(self, name):
        super.__init__(name)
        self.payoffs = []

    def getUtility():

