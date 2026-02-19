# lambda_with_sorted.py

students = [
    {"name": "Dias", "grade": 85},
    {"name": "Ali", "grade": 92},
    {"name": "Aruzhan", "grade": 78}
]

# Sort students by grade
sorted_students = sorted(students, key=lambda student: student["grade"])

print("Sorted students by grade:")
for student in sorted_students:
    print(student)
