# lambda_with_filter.py

numbers = [1, 2, 3, 4, 5, 6]

# Filter even numbers
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

print("Even numbers:", even_numbers)
