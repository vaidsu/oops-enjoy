#!/bin/python
from __future__ import unicode_literals
from prompt_toolkit import PromptSession
from collections import deque
from store import KVStore
import threading
from command import Command


class InMemDB:
    def __init__(self):
        self.stores = {'kv': KVStore()}
        self.tq = deque()
        self.lock = threading.Lock()
        self.command = Command(self.stores)

    def dispatch(self, store_type, cb=None):
        while True:
            try:
                self.lock.acquire()
                if self.tq:
                    action = self.tq.popleft()
                    t = threading.Thread(
                        target=action.fn,
                        args=(action.value),
                        kwargs={
                            'key': action.key,
                            'cb': cb
                        })
                    t.start()
            except KeyboardInterrupt:
                break

    def direct_dispatch(self, action, cb=None):
        return action.fn(action.value, key=action.key, cb=cb)

    def execute_command(self, cmd, value, key):
        if not cmd.endswith('ROLLBACK'):
            action = self.command.execute(cmd, value, key=key)
            self.lock.acquire()
            # self.tq.append(action)
            out = self.direct_dispatch(action)
            self.lock.release()
            print(out)
        else:
            print(self.command.execute(cmd))


def main():
    session = PromptSession()
    db = InMemDB()

    while True:
        try:
            text = session.prompt('> ')
        except KeyboardInterrupt:
            print('Press CTRL+D to exit')
            continue
        except EOFError:
            break
        else:
            if text.strip() == 'SHOW':
                print(db.command.show())
                continue
            query = text.split()
            if len(query) < 3:
                print('Syntax CMD VALUE KEY')
                continue
            cmd, value, key = query
            db.execute_command(cmd.strip(), value.strip(), key=key.strip())
    print('GoodBye!')


if __name__ == '__main__':
    main()
