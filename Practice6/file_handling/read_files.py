# This script reads a file in three different ways:
# read(), readline(), and readlines().

file_name = "sample.txt"

# read() reads the whole file at once
with open(file_name, "r", encoding="utf-8") as file:
    content = file.read()
    print("Using read():")
    print(content)

# readline() reads one line at a time
with open(file_name, "r", encoding="utf-8") as file:
    print("Using readline():")
    print(file.readline().strip())
    print(file.readline().strip())

# readlines() reads all lines and returns a list
with open(file_name, "r", encoding="utf-8") as file:
    print("Using readlines():")
    lines = file.readlines()

for index, line in enumerate(lines, start=1):
    print(f"{index}: {line.strip()}")