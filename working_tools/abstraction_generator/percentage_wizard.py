class PercentageWizard:
    def __init__(self, total_number_of_infosets, percentage):
        self.total_number_of_infosets = total_number_of_infosets
        self.percentage = percentage
        self.threshold = total_number_of_infosets * (1 - 2 * (1 - self.percentage))
        self.parsed_infosets = 0
        self.done_levels = 0

    def perform_clustering(self):
        if self.done_levels < 1:
            self.done_levels += 1
            return True
        return self.parsed_infosets >= self.threshold
