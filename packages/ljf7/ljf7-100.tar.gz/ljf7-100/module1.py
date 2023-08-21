def say_hello():
    print("Helllo,Wolrd!")

def fib(n):
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)