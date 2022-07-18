
class StorageSettings:
    def __init__(self, rows=100, racks_per_row=70, shelves_per_rack=10, shelf_size=200):
        self.rows = rows
        self.racks_per_row = racks_per_row
        self.shelves_per_rack = shelves_per_rack
        self.shelf_size = shelf_size

    def __str__(self):
        return "Storage Settings:\n" + \
               "     Rows: " + str(self.rows) + "\n" + \
               "     Racks Per Row: " + str(self.rows) + "\n" + \
               "     Shelves Per Rack: " + str(self.shelves_per_rack) + "\n" + \
               "     Shelf Size: " + str(self.shelf_size) + "\n"
