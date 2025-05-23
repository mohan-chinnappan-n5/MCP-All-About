# Decorators in python

- In Python, a decorator is a function that **wraps another function to extend or modify its behavior**. 
- Decorators are often used for logging, access control, timing, registering functions, etc.

```py
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

```