# class_variables.py

class Student:
    
    # Class variable
    school_name = "IT School"
    
    def __init__(self, name):
        self.name = name

# Creating objects
student1 = Student("Dias")
student2 = Student("Ali")

print(student1.name, "studies at", Student.school_name)
print(student2.name, "studies at", Student.school_name)
