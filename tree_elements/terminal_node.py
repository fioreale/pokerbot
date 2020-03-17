from tree_elements.node import Node


class TerminalNode(Node):

    def __init__(self):
        Node.__init__(self)
        self.payoffs = {}

    def createTerminalNode(self, history, payoffs, root):           # initialize a terminal node instance
        history_list = history.split('/')[1:]                       # deleted first empty element of the history
        self.history = history_list
        self.parent = root.node_finder(history_list[:-1])           # called node finder without last element (ASK LUCIANO!)
        self.parent.appendChild(self, history_list)
        payoffs_list = payoffs.split()
        for i in payoffs_list:
            payoffs_list = i.split('=')
            self.payoffs[payoffs_list[0]] = float(payoffs_list[1])  # dictionary indexed by player name
        return self

    def print_tree(self, level):                                    # override of the parent function to print payoffs
        l = 0
        while l < level:
            print('    ', end='')
            l += 1
        player = 1
        for payoff in self.payoffs.values():
            print(str(player) + '=' + str(payoff), end=' ')
            player += 1
        print('\n')