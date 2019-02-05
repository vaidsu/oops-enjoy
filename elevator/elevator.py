#!/bin/python
from enum import Enum
import threading
import random
import time


class Flow:
    def __init__(self):
        self.in_flow = 0
        self.out_flow = 0


class State(Enum):

    PRESSED = 1
    UNPRESSED = 2


class Panel:
    def __init__(self, num_floors):
        self.num_floors = num_floors
        self.state = [State.UNPRESSED for _ in range(self.num_floors)]
        self.lock = threading.Lock()

    def press(self, floor_num):
        # Press can be in panel or out panel, its all the same thing
        self.lock.acquire()
        self.state[floor_num] = State.PRESSED
        self.lock.release()

    def should_stop(self, floor_num):
        self.lock.acquire()
        state = self.state[floor_num]
        self.lock.release()
        return state == State.PRESSED

    def release(self, floor_num):
        self.lock.acquire()
        self.state[floor_num] = State.UNPRESSED
        self.lock.release()


class Elevator:
    def __init__(self, floors):
        self.floors = floors
        self.flow = [Flow() for _ in range(self.floors)]
        self.current = 0
        self.panel = Panel(self.floors)
        self.stop_elevator = False

    def call(self, floor_num, num_people, in_flow=False):
        # We call the elevator to enter in a particular floor
        # First we press the panel in or out, its all call for us,
        # it doesnt matter if users inside the elevator or outside
        self.panel.press(floor_num)
        # Update the flow in that floor
        if in_flow:
            self.flow[floor_num].in_flow += num_people
        else:
            self.flow[floor_num].out_flow += num_people

    def enter(self, floor_num):
        # Add the number of people current entering the floor
        # Reset the number of people entering
        self.current += self.flow[floor_num].in_flow
        self.flow[floor_num].in_flow = 0

    def exit(self, floor_num):
        # We set the elevator panel to a particular floor and then exit out
        self.current -= self.flow[floor_num].out_flow
        self.flow[floor_num].out_flow = 0

    def stop(self):
        self.stop_elevator = True

    def get_status(self):
        return self.current

    def start_simulation(self):
        t = threading.Thread(target=self.simulate)
        t.start()

    def simulate(self):
        # Move the elevator up or down depending on the pressed floors
        # The elevetor first goes up and the comes down fully, unless nothing
        # is pressed below it
        while self.stop_elevator is False:
            for i in range(self.floors):
                if self.panel.should_stop(i):
                    print('Stopping in floor {}'.format(i))
                    self.exit(i)
                    self.enter(i)
                    self.panel.release(i)
                    print('| {} |'.format(self.get_status()))
                    time.sleep(1)
            for i in range(self.floors - 1, -1, -1):
                if self.panel.should_stop(i):
                    print('Stopping in floor {}'.format(i))
                    self.exit(i)
                    self.enter(i)
                    self.panel.release(i)
                    print('| {} |'.format(self.get_status()))
                    time.sleep(1)
        print('Simulation stopped')


elevator = Elevator(10)
# Start the lift
elevator.start_simulation()
# Call randomly
elevator.call(4, 5, in_flow=True)
time.sleep(2)
elevator.call(3, 3, in_flow=True)
time.sleep(2)
elevator.call(9, 5, in_flow=False)
time.sleep(2)
elevator.call(2, 2, in_flow=False)
time.sleep(2)
# Stop the elevator
elevator.stop()
