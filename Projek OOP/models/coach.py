class Coach:
    def __init__(self, name, age, experience):
        self.name = name
        self.age = age
        self.experience = experience

    def show_info(self):
        return f"{self.name.title()}, {self.age} yrs old, {self.experience} years of experience"

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "experience": self.experience
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["age"],
            data["experience"]
        )
