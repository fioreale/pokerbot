import utilities

class InfoStructure:  # list of information sets of player1 and player2
    def __init__(self):
        self.infoSets1 = []
        self.infoSets2 = []
        self.chances = []

    def appendInfoSet(self, list, infoset):
        list.append(infoset)

    def assignInfoSet(self, infoset, root):
        history = list(infoset.infoNodes.keys())[0].split('/')[1:]
        if len(infoset.name) < 4:
            self.appendInfoSet(self.infoSets1, infoset)
        else:
            # assigned = utilities.in_chars(infoset.name.split(':')[-2])[-1]
            current_player = root.node_finder(history).getPlayer()
            if current_player == '1':
                self.appendInfoSet(self.infoSets1, infoset)
            elif current_player == '2':
                self.appendInfoSet(self.infoSets2, infoset)
            else:
                self.appendInfoSet(self.chances, infoset)

