# This script creates a text file and writes sample data into it.
# "w" mode means write mode. If the file exists, old content is replaced.

file_name = "sample.txt"

with open(file_name, "w", encoding="utf-8") as file:
    file.write("Python File Handling Practice\n")
    file.write("This is the first line.\n")
    file.write("This is the second line.\n")

print("File created and data written.")

# "a" mode means append mode.
# It adds new text to the end of the file without deleting old content.
with open(file_name, "a", encoding="utf-8") as file:
    file.write("This line was added later.\n")
    file.write("Append mode keeps previous content.\n")

print("New lines appended.")