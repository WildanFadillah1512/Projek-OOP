from abc import ABC

class Player:
    def __init__(self, name, age, number, position):
        self.name = name
        self.age = age
        self.number = number
        self.position = position

    def show_info(self):
        return f"{self.name.title()}, #{self.number} - {self.position.title()}, {self.age} yrs old"

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "number": self.number,
            "position": self.position
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["age"],
            data["number"],
            data["position"]
        )