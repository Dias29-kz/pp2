# This script copies a file into another folder
# and searches for .txt files.

import shutil
from pathlib import Path

source_file = Path("../file_handling/sample.txt")
target_folder = Path("collected_files")

# Create target folder if it does not exist
target_folder.mkdir(exist_ok=True)

# Copy file into the new folder
if source_file.exists():
    shutil.copy(source_file, target_folder / source_file.name)
    print("File copied to collected_files folder.")
else:
    print("Source file not found.")

# Search for all .txt files
print("\nTXT files found:")
for file in Path(".").rglob("*.txt"):
    print(file)