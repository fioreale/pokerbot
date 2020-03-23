import utilities


class InfoStructure:  # list of information sets of player1 and player2
    def __init__(self):
        self.infoSets1 = []
        self.infoSets2 = []

    def append_info_set(self, list, infoset):
        list.append(infoset)

    def assign_info_set(self, infoset, root):
        history = list(infoset.infoNodes.keys())[0].split('/')[1:]
        if len(infoset.name) < 4:
            self.append_info_set(self.infoSets1, infoset)
        else:
            # assigned = utilities.in_chars(infoset.name.split(':')[-2])[-1]
            current_player = root.node_finder(history).getPlayer()
            if current_player == '1':
                self.append_info_set(self.infoSets1, infoset)
            else:
                self.append_info_set(self.infoSets2, infoset)

