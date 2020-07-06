class PercentageWizard:

    def __init__(self, total_number_of_infosets, clusterization_percentage):
        self.total_number_of_infosets = total_number_of_infosets
        self.clusterization_percentage = clusterization_percentage
        self.parsed_infosets = 0
        self.threshold = total_number_of_infosets - 2*(1-clusterization_percentage)*total_number_of_infosets

    def clusterization_start(self):
        if self.parsed_infosets == 0:
            return True
        return self.parsed_infosets >= self.threshold
