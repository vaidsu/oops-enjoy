#!/bin/python
from __future__ import unicode_literals
from prompt_toolkit import prompt
from payment import Payment
from vehicle import VehicleFactory
from slots import SlotSize
import random
import string
import time


class ParkingLot:
    def __init__(self, num_floors, num_slots):
        self.lot = [[None for _ in range(num_slots)]
                    for _ in range(num_floors)]
        self.num_floors = num_floors
        self.num_slots = num_slots
        self.payment = Payment()
        self.filled = 0
        self.vehicles = VehicleFactory()

    def is_full(self):
        return self.filled == self.num_slots * self.num_floors

    def find_slot(self, vehicle):
        got_slot = False
        while got_slot is False:
            floor = random.randrange(0, self.num_floors)
            slot = random.randrange(0, self.num_slots)
            if self.lot[floor][slot] is not None:
                continue
            got_slot = vehicle.does_it_fit(
                random.choice([i.value for i in list(SlotSize)]))
        return floor, slot

    def enter(self, plate, vehicle_type, is_flat=False):
        if self.is_full():
            raise AssertionError('Parking lot full>>>')

        # On entering the user gets a new ticket
        ticket = self.payment.get_ticket(plate, is_flat=is_flat)
        # We got the ticket now put the ticket into the vehicle
        vehicle = self.vehicles(vehicle_type, plate, ticket)
        # Get a slot
        floor, slot = self.find_slot(vehicle)
        # Put the slot
        vehicle.floor = floor
        vehicle.slot = slot
        # Use up a slot
        self.filled += 1
        # Add the slot
        self.lot[floor][slot] = plate
        # Return the vehicle
        return vehicle

    def exit(self, vehicle):
        # Vehicle is exiting so release the slot
        self.lot[vehicle.floor][vehicle.slot] = None
        # Reduce the filled
        self.filled -= 1
        # Get the money
        self.payment.release_ticket(vehicle.ticket)
        # Done

    def close(self):
        # Close for the day
        return self.payment.money

    def get_current_slot(self):
        for f in range(self.num_floors):
            print('{}==>'.format(f), end='')
            for s in range(self.num_slots):
                print(
                    '| {} |'.format(' ' if self.lot[f][s] is None else
                                    self.lot[f][s]),
                    end='')
            print('')


lot = ParkingLot(10, 10)
print(lot.get_current_slot())
vehicles = []
for i in string.ascii_lowercase:
    vehicles.append(
        lot.enter(
            i, random.choice(['bike', 'compact', 'large', 'truck',
                              'trailer'])))
time.sleep(random.randrange(10))
print(lot.get_current_slot())
for v in vehicles:
    lot.exit(v)
print(lot.close())
