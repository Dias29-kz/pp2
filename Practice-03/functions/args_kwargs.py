# args_kwargs.py

# Function using *args (multiple positional arguments)
def add_all_numbers(*args):
    total = sum(args)
    print("Sum of all numbers:", total)

# Function using **kwargs (multiple keyword arguments)
def print_user_info(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)

# Calling functions
add_all_numbers(1, 2, 3, 4, 5)

print_user_info(name="Dias", age=18, country="Kazakhstan")
