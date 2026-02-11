grade = float(input("Enter your grade: "))

def value_of_the_grade(grade):
    if 9 <= grade <= 10:
        value = "A"
    elif 7 <= grade <= 8.9:
        value = "B"
    elif 5 <= grade <= 6.9:
        value = "C"
    elif 3 <= grade <= 4.9:
        value = "D"
    elif 0 <= grade <= 2.9:
        value = "F"
    return value

print("The value for the grade", grade, "is", value_of_the_grade(grade))

#9.5, 7.0, 5.5, 3.2, 1.0 (grades to try)