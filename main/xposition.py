class XPosition(str):
    to_number_map = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
    to_letter_map = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}

    def __sub__(self, other: int):
        new_value = self.to_number_map[self] - other

        if new_value not in self.to_letter_map:
            return XPosition("")
        return XPosition(self.to_letter_map[new_value])

    def __add__(self, other: int):
        new_value = self.to_number_map[self] + other

        if new_value not in self.to_letter_map:
            return XPosition("")
        return XPosition(self.to_letter_map[new_value])
