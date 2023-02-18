from enum import Enum


class State(Enum):
    # Find new beginning states
    Q0 = 1
    Q1 = 2
    Qa = 3
    Qr = 4

    # Fill down states
    D0 = 5
    D1 = 6
    D2 = 7
    D3 = 8
    D4 = 9
    D5 = 10
    D6 = 11
    D7 = 12
    D8 = 13
    Da = 14
    Dr = 15
