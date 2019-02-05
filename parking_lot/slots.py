#!/bin/python
from enum import Enum, IntEnum


class SlotSize(IntEnum):
    BIKE = 1
    COMPACT = 2
    LARGE = 3
    TRUCK = 4
    TRAILER = 5


class SlotState(Enum):
    OPEN = 1
    CLOSED = 2


class Slot():
    def __init__(self, size: SlotSize):
        self.size = size
        self._state = SlotState.OPEN

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: SlotState):
        self._state = state

    @state.getter
    def state(self, state: SlotState):
        self._state = state
