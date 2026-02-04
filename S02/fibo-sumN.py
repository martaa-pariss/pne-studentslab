def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def fibosum(n):
    sum = 0
    for i in range(0, n):
        sum += fibonacci(i)
    return sum

print("la suma de fibonacci de los primeros 10 numeros es:", fibosum(11))
print("la suma de fibonacci de los primeros 5 numeros es:", fibosum(6))