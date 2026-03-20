# This script copies a file, creates a backup, and deletes a copied file safely.

import os
import shutil

source_file = "sample.txt"
copied_file = "sample_copy.txt"
backup_file = "sample_backup.txt"

# Copy the original file
if os.path.exists(source_file):
    shutil.copy(source_file, copied_file)
    print("File copied successfully.")

    shutil.copy(source_file, backup_file)
    print("Backup created successfully.")
else:
    print("Source file not found.")

# Delete copied file safely
if os.path.exists(copied_file):
    os.remove(copied_file)
    print("Copied file deleted safely.")
else:
    print("Copied file does not exist.")