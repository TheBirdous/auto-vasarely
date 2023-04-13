"""
Contains states used by automata implemented in the recognition module.

Author: Marek Dohnal

Date: 20/03/2023
"""

from enum import Enum, auto


class State(Enum):
    """
    Represents the states used by the four-way automata
    as defined by their transition diagrams
    """

    # Find new beginning states
    S0 = auto()
    S1 = auto()
    Sa = auto()
    Sr = auto()

    # Fill down states
    D0 = auto()
    D1 = auto()
    D2 = auto()
    D3 = auto()
    D4 = auto()
    D5 = auto()
    D6 = auto()
    D7 = auto()
    D8 = auto()
    Da = auto()
    Dr = auto()

    # Fill up states
    U0 = auto()
    U1 = auto()
    U2 = auto()
    U3 = auto()
    U4 = auto()
    Ua = auto()
    Ur = auto()

    # Find new F_B states
    N0 = auto()
    N1 = auto()
    N2 = auto()
    N3 = auto()
    N4 = auto()
    N5 = auto()
    N6 = auto()
    Na = auto()
    Nr = auto()