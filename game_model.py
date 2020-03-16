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


class Node(object):
    def __init__(self):
        self.action = []
        self.children = []
        self.infoset = []
        self.signals = []
        self.parent = None
        self.card1 = None # possible to be added just on the root node without creating to much space for every node
        self.card2 = None
        self.card3 = None
        self.payoff1 = None  # if terminal
        self.payoff2 = None

    def setRoot(actions):
        value = actions.split()

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