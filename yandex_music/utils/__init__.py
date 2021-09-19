from dataclasses import dataclass


def model(cls):
    return dataclass(cls, eq=False, repr=False)
