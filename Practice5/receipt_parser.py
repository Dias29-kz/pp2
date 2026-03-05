import re

# Open the file raw.txt in read mode
file = open("raw.txt", "r")

# Read the file line by line
for line in file:
    # Remove spaces/newline and print the line
    print(line.strip())

# Close the file
file.close()


# Example text for RegEx practice
text = "Milk 500 Bread 300 Apple 700"


# search – finds the first number in the text
x = re.search(r"\d+", text)
print("search:", x.group())


# findall – finds all numbers in the text
x = re.findall(r"\d+", text)
print("findall:", x)


# split – splits the text by spaces
x = re.split(r"\s", text)
print("split:", x)


# sub – replaces numbers with the word PRICE
x = re.sub(r"\d+", "PRICE", text)
print("sub:", x)


# -------- Receipt Parsing --------

# Read the entire receipt file
with open("raw.txt") as f:
    receipt = f.read()

# Extract all prices from the receipt
prices = re.findall(r"\d+", receipt)

# Extract product names
products = re.findall(r"[A-Za-z]+", receipt)

print("Products:", products)
print("Prices:", prices)

# Calculate total amount
total = sum(map(int, prices))

print("Total:", total)



