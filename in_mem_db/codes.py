#!/bin/python

from enum import IntEnum


class Codes(IntEnum):

    SUCCESS = 1
    FAILURE = 2
    UPDATE = 3
    ROLLBACK = 4
    INVALID_INPUT = 5
    KEY_NOT_EXIST = 6
    ACTION_IGNORED = 7
    UNKNOWN = 8


FAILURES = [
    Codes.FAILURE, Codes.INVALID_INPUT, Codes.KEY_NOT_EXIST,
    Codes.ACTION_IGNORED, Codes.UNKNOWN
]
