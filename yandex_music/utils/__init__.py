from dataclasses import dataclass


def model(cls):  # noqa: ANN001, ANN201
    return dataclass(cls, eq=False, repr=False)
