# modules/inventory/subscribers.py

from modules.inventory.projection import apply_event


def inventory_subscriber(event):

    apply_event(event)