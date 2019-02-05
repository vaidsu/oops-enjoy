#!/bin/python

from store import Action


class Command:
    def __init__(self, store):
        self.store = store

    def show(self):
        return ','.join(
            [i.upper() for i in dir(self) if i != 'execute' and not i.startswith('_')])

    def kset(self, value, key):
        return Action(self.store['kv'].set, value, key=key)

    def kget(self, value, key):
        return Action(self.store['kv'].get, value, key=key)

    def kpop(self, value, key):
        return Action(self.store['kv'].remove, None, key=key)

    def krollback(self, *args, **kwargs):
        return self.store['kv'].rollback()

    def execute(self, cmd, *args, **kwargs):
        if cmd.lower() not in dir(self):
            return False
        return getattr(self, cmd.lower())(*args, **kwargs)
