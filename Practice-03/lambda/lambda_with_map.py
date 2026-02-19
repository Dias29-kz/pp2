# lambda_with_map.py

numbers = [1, 2, 3, 4, 5]

# Using lambda with map to square numbers
squared = list(map(lambda x: x * x, numbers))

print("Squared numbers:", squared)
