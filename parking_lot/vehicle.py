#!/bin/python
from abc import ABC, abstractmethod
from slots import SlotSize
from payment import Ticket


class Vehicle(ABC):
    def __init__(self, plate: str, ticket: Ticket):
        self.plate = plate
        self.ticket = ticket
        self.floor = None
        self.slot = None

    @abstractmethod
    def does_it_fit(self, slot_size: int):
        pass


class VehicleFactory():
    def __call__(self, type, plate, ticket):
        if type == 'bike':
            return Bike(plate, ticket)
        elif type == 'compact':
            return Compact(plate, ticket)
        elif type == 'large':
            return Large(plate, ticket)
        elif type == 'truck':
            return Truck(plate, ticket)
        else:
            return Trailer(plate, ticket)


class Bike(Vehicle):
    def does_it_fit(self, slot_size):
        return True


class Compact(Vehicle):
    def does_it_fit(self, slot_size):
        return slot_size > SlotSize.BIKE


class Large(Vehicle):
    def does_it_fit(self, slot_size):
        return slot_size > SlotSize.COMPACT


class Truck(Vehicle):
    def does_it_fit(self, slot_size):
        return slot_size > SlotSize.LARGE


class Trailer(Vehicle):
    def does_it_fit(self, slot_size):
        return slot_size > SlotSize.TRUCK
