# This script demonstrates map(), filter(), reduce(),
# and some common built-in functions.

from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# map() applies a function to every element
squared = list(map(lambda x: x * x, numbers))
print("Squared numbers:", squared)

# filter() keeps only elements that match the condition
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)

# reduce() combines all elements into one result
total = reduce(lambda a, b: a + b, numbers)
print("Sum using reduce():", total)

# Other built-in functions
print("Length:", len(numbers))
print("Sum:", sum(numbers))
print("Min:", min(numbers))
print("Max:", max(numbers))
print("Sorted descending:", sorted(numbers, reverse=True))

# Type checking and conversion
text_number = "25"
print("Type before conversion:", type(text_number))

converted_number = int(text_number)
print("Converted value:", converted_number)
print("Type after conversion:", type(converted_number))