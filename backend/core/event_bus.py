import asyncio
import logging

class EventBus:
    def __init__(self):
        self.subscribers = {}
        self.logger = logging.getLogger("EventBus")

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        self.logger.info(f"Subscribed to {event_type}")

    async def publish(self, event_type, data):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                await callback(data)
        self.logger.info(f"Published event: {event_type}")
