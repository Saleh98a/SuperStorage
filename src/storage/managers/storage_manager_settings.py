"""
Storage Manager Settings
"""

class StorageManagerSettings:

    def __init__(self, insert_algorithm, extract_algorithm, sector_bounds=None, learned_info=None):
        if sector_bounds is None:
            sector_bounds = []

        if learned_info is None:
            learned_info = []

        self.insert_algorithm = insert_algorithm
        self.extract_algorithm = extract_algorithm
        self.sector_bounds = sector_bounds
        self.learned_info = learned_info


    def __str__(self):
        return "Insert: " + str(self.insert_algorithm) + "\n" + \
            "Extract: " + str(self.extract_algorithm) + "\n" + \
            "Sector Bounds: " + str(self.sector_bounds) + "\n"
            # "Learned Info: " + str(self.learned_info) + "\n"


