n = 0
flag = True
while flag:
    if n == 0:
        print("0")
        n += 1
    elif n == 1:
        print("1")
        n += 1
    elif n == 12:
        flag = False
    else:
        n = (n-1) + (n-2)
        print(n)
        n += 1