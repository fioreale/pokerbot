import utilities

class InfoStructure:  # list of information sets of player1 and player2
    def __init__(self):
        self.infoSets1 = []
        self.infoSets2 = []
        self.chances = []

    def appendInfoSet(self, list, infoset):
        list.append(infoset)

    def assignInfoSet(self, infoset):
        if len(infoset.name) < 4:
            self.appendInfoSet(self.chances, infoset)
        else:
            assigned = utilities.in_chars(infoset.name.split(':')[-2])[-1]
            if assigned == '1':
                self.appendInfoSet(self.infoSets1, infoset)
            elif assigned == '2':
                self.appendInfoSet(self.infoSets2, infoset)
            else:
                self.appendInfoSet(self.chances, infoset)
