class PokerGame:
    def __init__(self):
        self.players = []
        self.deck = []
        self.tree = None
        self.infoStructure = None
        self.actions = []


class Card:
    def __init__(self):
        self.cardName = None
        self.value = None

    def getValue(self):


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
        self.actions = []
        self.children = {}
        self.infoset = []
        self.signals = {}
        self.parent = None
        #self.card1 = None # possible to be added just on the root node without creating to much space for every node
        #self.card2 = None
        #self.card3 = None
        self.cards = []
        self.payoffs = []

    def node_finder(self, history):
        if len(history) == 1:
            return self.children[history[0]]
        else:
            for i in self.children.items():
                if i.name == history[0]:
                    return i.node_finder(i, history[1:])
            return None

    def setRoot(self, actions):
        values = actions.split()
        for i in values :
            splitted_values = i.split('=')
            self.children[splitted_values[0]] = Node('C:'+splitted_values[0])
            self.children[splitted_values[0]].setCards(splitted_values[1])
            self.signals[splitted_values[0]] = splitted_values[1]
            self.actions.append(splitted_values[1])
        sum = 0
        for j in self.signals :
            sum += self.signals[j]
        for k in self.signals :
            self.signals[k] = self.signals[k]/sum

    def setActionNode(self, history, actions, root):
        history_splitted = history.split('/')
        self.parent = root.node_finder(history_splitted[1:])
        actions_splitted = actions.split()
        for i in actions_splitted :
            self.actions.append(actions_splitted[i])
        self.cards = self.parent.getCards()

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


    def appendCards(self, cards):
        self.cards.append(cards)

    def getCards(self):
        return self.cards

    def setCards(self, cards):
        self.cards = cards

    def nextNode(action):

    def getParent():

    def getActions():

    def getPlayer():

    def getUtility():

    def getCurrentNode():

    def setNextNode(self, action):

    def setParent(Tree):

    def setActions():


class NatureNode(Node):
    def __init__(self):
        self.children = []
        self.parent = None


class PlayerNode(Node):


class TerminalNode(Node):


