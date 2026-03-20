# This script demonstrates enumerate() and zip().

students = ["Dias", "Ali", "Aruzhan"]
scores = [90, 85, 95]
subjects = ["Math", "Python", "English"]

# enumerate() gives index and value together
print("Using enumerate():")
for index, student in enumerate(students, start=1):
    print(index, student)

# zip() combines lists element by element
print("\nUsing zip():")
for student, score in zip(students, scores):
    print(student, score)

# zip() can combine three lists too
print("\nUsing zip() with three lists:")
for student, score, subject in zip(students, scores, subjects):
    print(student, score, subject)