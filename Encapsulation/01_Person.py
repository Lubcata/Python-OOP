class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.__age = age

    def get_name(self):
        return self.name

    def get_age(self):
        return self.__age


person = Person("George", 32)
print(person.get_name())
print(person.get_age())

