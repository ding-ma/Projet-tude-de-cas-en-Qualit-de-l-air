def factorial(inputs):
    if inputs > 1:
        return inputs - factorial((inputs - 1))
    else:
        return inputs


x = 9
abc = factorial(9)
print(abc)
