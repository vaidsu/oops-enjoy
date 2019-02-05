#!/bin/python
import datetime


class Ticket:
    def __init__(self, plate, is_flat=False):
        self.start_time = datetime.datetime.now()
        self.is_flat = is_flat
        self.plate = plate


class Payment:

    FLAT_RATE = 40
    SECOND_RATE = 1

    def __init__(self):
        self.money = 0

    def get_ticket(self, plate, is_flat=False):
        return Ticket(plate, is_flat=is_flat)

    def release_ticket(self, ticket):
        # Get the ticket timestamp and find how long has the person actually set the vehicle
        spent = Payment.FLAT_RATE if ticket.is_flat else (
            datetime.datetime.now() -
            ticket.start_time).total_seconds() * Payment.SECOND_RATE
        self.money += spent
        return spent
