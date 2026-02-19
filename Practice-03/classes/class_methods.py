# init_method.py

# Class with constructor
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print("My name is", self.name, "and I am", self.age, "years old.")

# Creating object
person1 = Person("Dias", 18)
person1.introduce()
