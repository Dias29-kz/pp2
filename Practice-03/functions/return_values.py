# return_values.py

# Function that returns a value
def square(number):
    return number * number

# Function that returns multiple values
def get_full_name(first_name, last_name):
    return first_name + " " + last_name

# Using returned values
result = square(5)
print("Square is:", result)

full_name = get_full_name("Dias", "Igibay")
print("Full name:", full_name)
