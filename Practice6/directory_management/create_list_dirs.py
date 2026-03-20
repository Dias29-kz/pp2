# This script creates directories and lists files/folders.

import os
from pathlib import Path

# Create one folder
if not os.path.exists("demo_folder"):
    os.mkdir("demo_folder")

# Create nested folders
os.makedirs("demo_folder/subfolder/inner_folder", exist_ok=True)

print("Directories created.")

# Show current working directory
print("Current directory:", os.getcwd())

# List all items in the current directory
print("\nItems in current directory:")
for item in os.listdir("."):
    print(item)

# Find Python files using pathlib
print("\nPython files:")
for py_file in Path(".").glob("*.py"):
    print(py_file)