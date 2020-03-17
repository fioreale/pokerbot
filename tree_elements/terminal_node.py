from tree_elements.node import Node



class TerminalNode(Node):

    def __init__(self):
        Node.__init__(self)
        self.payoffs = {}

    def createTerminalNode(self, history, payoffs, root):
        history_list = history.split('/')[1:]
        self.history = history_list
        self.parent = root.node_finder(history_list[:-1])
        self.parent.appendChild(self, history_list)
        payoffs_list = payoffs.split()
        for i in payoffs_list:
            payoffs_list = i.split('=')
            self.payoffs[payoffs_list[0]] = float(payoffs_list[1])
        return self

    def print_tree(self, level):
        l = 0
        while (l < level):
            print('    ', end='')
            l += 1
        player = 1
        for payoff in self.payoffs.values():
            print(str(player) + '=' + str(payoff), end = ' ')
            player += 1
        print('\n')