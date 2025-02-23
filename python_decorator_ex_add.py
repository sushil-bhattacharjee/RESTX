def add_five(test):
    def bigdeal(*args, **kwargs):
        print("Starting Decorator function bigdeal")
        print("Bringing func test in next line")
        result = test(*args, **kwargs)
        return result + 5
        
    return bigdeal

@add_five
def test():
    return 10

print(test())