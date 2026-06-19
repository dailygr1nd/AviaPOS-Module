# core/events/bus.py

subscribers = []


def subscribe(handler):

    subscribers.append(handler)


def publish(event):

    for subscriber in subscribers:
        subscriber(event)

from core.events.bus import subscribe
from modules.inventory.subscribers import inventory_subscriber

subscribe(inventory_subscriber)