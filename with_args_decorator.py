# This is a simple example of a decorator in Python.
# Decorators are a way to modify or enhance functions or methods without changing their code.
# They are often used for logging, access control, memoization, and other cross-cutting concerns.
#
# In this example, we will create a simple decorator that prints a message before and after the function runs.
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

# Usage of the decorator
# The decorator is applied to the function greet, which takes a name as an argument and prints a greeting message.
@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")