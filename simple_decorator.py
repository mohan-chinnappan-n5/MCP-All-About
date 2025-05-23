# This is a simple example of a decorator in Python.
# Decorators are a way to modify or enhance functions or methods without changing their code.
# They are often used for logging, access control, memoization, and other cross-cutting concerns.

# A decorator is a function that takes another function as an argument and returns a new function that adds some kind of functionality to the original function.

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function runs")
        result = func(*args, **kwargs)
        print("After the function runs")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()