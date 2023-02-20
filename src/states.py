from enum import Enum, auto


class State(Enum):
    # Find new beginning states
    Q0 = auto()
    Q1 = auto()
    Qa = auto()
    Qr = auto()

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