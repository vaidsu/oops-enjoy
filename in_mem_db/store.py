#!/bin/python
from abc import ABC, abstractmethod
from codes import Codes
import threading


class Action:
    def __init__(self, fn, value, key=None):
        self.name = fn.__name__
        self.fn = fn
        self.value = value
        self.key = key

    def __repr__(self):
        return 'name: {} value: {} key: {}'.format(self.name, self.value,
                                                   self.key)


class Response:
    def __init__(self, prev_state, new_state, rc, return_val):
        self.code = rc
        self.prev_state = prev_state
        self.new_state = new_state
        self.return_val = return_val

    def __repr__(self):
        return 'prev: {}, new: {}, rc: {}, return: {}'.format(
            self.prev_state, self.new_state, self.code, self.return_val)


class Store(ABC):
    def __init__(self):
        self.ds = None
        self.lock = threading.Lock()
        self.tlog = []  # Prev action and response

    @abstractmethod
    def set(self, value, key=None, expiry=None) -> Response:
        pass

    @abstractmethod
    def get(self, value, key=None) -> Response:
        pass

    @abstractmethod
    def remove(self, value, key=None) -> Response:
        pass

    @abstractmethod
    def rollback(self, prev_action: Action,
                 prev_response: Response) -> Response:
        pass

    def __repr__(self):
        pass


class KVStore(Store):
    def __init__(self):
        self.ds = {}
        self.lock = threading.Lock()
        self.tlog = []

    def set(self, value, key=None, cb=None, expiry=None):
        if not key:
            if cb:
                cb(Codes.INVALID_INPUT)
            return Response(None, None, Codes.INVALID_INPUT, None)
        self.lock.acquire()
        if key in self.ds:
            out = Response(self.ds[key], value, Codes.UPDATE, None)
        else:
            out = Response(None, value, Codes.SUCCESS, None)
        self.ds[key] = value
        self.lock.release()
        if cb:
            cb(out.code)
        self.tlog.append((Action(self.set, value, key=key), out))
        return out

    def get(self, value, key=None, cb=None):
        if not key:
            if cb:
                cb(Codes.INVALID_INPUT)
            return Response(None, None, Codes.INVALID_INPUT, None)
        self.lock.acquire()
        ds = self.ds
        self.lock.release()
        if key not in ds:
            if cb:
                cb(Codes.KEY_NOT_EXIST)
            return Response(None, None, Codes.KEY_NOT_EXIST, None)
        if cb:
            cb(Codes.SUCCESS)
        return Response(None, None, Codes.SUCCESS, ds[key])

    def remove(self, value, key=None, cb=None):
        if not key:
            if cb:
                cb(Codes.INVALID_INPUT)
            return Response(None, None, Codes.INVALID_INPUT, None)
        self.lock.acquire()
        ds = self.ds
        self.lock.release()
        if key not in ds:
            if cb:
                cb(Codes.KEY_NOT_EXIST)
            return Response(None, None, Codes.KEY_NOT_EXIST, None)
        self.lock.acquire()
        out = Response(self.ds[key], None, Codes.SUCCESS, None)
        self.ds.pop(key)
        self.lock.release()
        if cb:
            cb(Codes.SUCCESS)
        self.tlog.append((Action(self.remove, value, key=key), out))
        return out

    def rollback(self):
        if not self.tlog:
            print('Nothing to rollback')
            return Response(None, None, Codes.FAILURE, None)
        prev_action, prev_response = self.tlog.pop()
        print('Rollback for {} {}'.format(prev_action, prev_response))
        if prev_action.name == 'set':
            # Rollback to remove or reset
            if prev_response.code == Codes.SUCCESS:
                # This is a brand new set, so simply remove it
                return self.remove(prev_response.new_state)
            elif prev_response.code == Codes.UPDATE:
                # This is update, so revert to old value
                return self.set(prev_response.prev_state, key=prev_action.key)
        elif prev_action.name == 'remove':
            if prev_response.code == Codes.SUCCESS:
                return self.set(prev_response.prev_state, key=prev_action.key)

        return Response(None, None, Codes.UNKNOWN, None)
