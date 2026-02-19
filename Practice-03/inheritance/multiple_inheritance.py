# multiple_inheritance.py

class Father:
    def skills(self):
        print("Programming")

class Mother:
    def talents(self):
        print("Design")

class Child(Father, Mother):
    pass

child = Child()
child.skills()
child.talents()
