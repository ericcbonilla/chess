A = 1
B = 2
C = 3
D = 4
E = 5
F = 6
G = 7
H = 8
TO_INT = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
TO_STR = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}


def to_int(x: str):
    return TO_INT[x]


def to_str(x: int):
    return TO_STR[x]
