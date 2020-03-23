import utilities


class InfoStructure:  # list of information sets of player1 and player2
    def __init__(self):
        self.info_sets1 = []
        self.info_sets2 = []

    def append_info_set(self, list, infoset):
        list.append(infoset)

    def assign_info_set(self, infoset, root):
        history = list(infoset.infoNodes.keys())[0].split('/')[1:]
        if len(infoset.name) < 4:
            self.append_info_set(self.info_sets1, infoset)
        else:
            current_player = root.node_finder(history).get_player()
            if current_player == '1':
                self.append_info_set(self.info_sets1, infoset)
            else:
                self.append_info_set(self.info_sets2, infoset)

