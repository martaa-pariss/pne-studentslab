#a)
def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False
number = int(input("Enter a number: "))
output = is_even(number)
print("Is the number", number, "even?", output)
    #try with: 4, 7, 0, -3, 10

#b)
def classify_triangle(a, b, c):
    if a == b and b == c:
        value = "Equilateral"
    elif a == b or b == c or a == c:
        value = "Isosceles"
    else:
        value = "Scalene"

print("The triangle with sides 5,5,5 is", classify_triangle(5, 5, 5))
print("The triangle with sides 3,3,4 is", classify_triangle(3, 3, 4))
print("The triangle with sides 3,4,5 is", classify_triangle(3, 4, 5))
