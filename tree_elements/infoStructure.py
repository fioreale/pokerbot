# This class is used to build the entire infostructure of the game.
# The infostructure of the game contains the infosets of all the player


class InfoStructure:
    def __init__(self):
        # infosets list for player 1
        self.info_sets1 = []
        # infosets list for player 2
        self.info_sets2 = []

    # TODO could be deleted, see comments where it is used
    def append_info_set(self, list, infoset):
        list.append(infoset)

    def assign_info_set(self, infoset, root):
        history = list(infoset.info_nodes.keys())[0].split('/')[1:]
        if len(infoset.name) < 4:
            # self.info_sets1.append(infoset)
            self.append_info_set(self.info_sets1, infoset)
        else:
            current_player = root.node_finder(history).player
            if current_player == '1':
                # self.info_sets1.append(infoset)
                self.append_info_set(self.info_sets1, infoset)
            else:
                # self.info_sets2.append(infoset)
                self.append_info_set(self.info_sets2, infoset)
