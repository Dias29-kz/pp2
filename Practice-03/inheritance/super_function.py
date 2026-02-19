# super_function.py

class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

    def display(self):
        print("Name:", self.name)
        print("Grade:", self.grade)

student1 = Student("Dias", 95)
student1.display()
