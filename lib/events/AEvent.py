from abc import ABC, abstractmethod

import discord


class AEvent(ABC):
    def __init__(self):
        self.run = self.disabled_action
        super().__init__()

    def enable_event(self):
        self.run = lambda m: self.enabled_action(m)

    def disable_event(self):
        self.run = self.disabled_action

    async def execute(self, i: list):
        await self.run(i)

    @abstractmethod
    async def enabled_action(self, args: list):
        raise NotImplementedError

    async def disabled_action(self, args: list):
        pass
