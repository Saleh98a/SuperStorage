"""
Rack model (Rack is basically a list of shelves)
"""
from src.events.event_bus import EventBus
from src.models.shelf import Shelf


class Rack:
    def __init__(self, num_of_shelves, shelf_size):
        self.num_of_shelves = num_of_shelves
        self.shelf_size = shelf_size
        self.event_bus = EventBus()
        self.shelves = [Shelf(shelf_size, self.event_bus) for _ in range(num_of_shelves)]
        self.used_size = 0
        self.activity = 0
        self.insert_activity = 0
        self.extract_activity = 0
        self.activity = 0
        self.set_handlers()

    def set_handlers(self):
        self.event_bus.subscribe('shelf_package_inserted', self.package_inserted_handler)
        self.event_bus.subscribe('shelf_order_extracted', self.order_extracted_handler)

    def package_inserted_handler(self, shelf, package):
        self.used_size += package.size()
        self.activity = self.activity + 1
        self.insert_activity = self.insert_activity + 1

    def order_extracted_handler(self, shelf, item, quantity):
        self.used_size -= quantity * item.size
        self.activity = self.activity + 1
        self.extract_activity = self.extract_activity + 1

    def is_used(self):
        return self.used_size != 0


