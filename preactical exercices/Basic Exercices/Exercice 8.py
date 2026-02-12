students = [
    {"name": "Ana", "grades": [8.5, 7.0, 9.0]},
    {"name": "Luis", "grades": [5.0, 4.5, 6.0]},
    {"name": "Maria", "grades": [9.5, 9.0, 10.0]},
    {"name": "Pedro", "grades": [3.0, 4.0, 2.5]},
    {"name": "Sofia", "grades": [7.0, 7.5, 8.0]},
]
for student in students:
    average = sum(student["grades"])/ len(student["grades"])
    average = round(average, 2)
    student["average"] = average
    if average < 5.00:
        grade_value = ("Fail")
    elif average >= 5.00:
        grade_value = ("Pass")
    student["pass or fail"] = grade_value

for student in students:
    print(f"{student['name']}: {student['average']} -> {student['pass or fail']}")

print("---------------------------")

########################################################################
#ben fet

students = [
    {"name": "Ana", "grades": [8.5, 7.0, 9.0]},
    {"name": "Luis", "grades": [5.0, 4.5, 6.0]},
    {"name": "Maria", "grades": [9.5, 9.0, 10.0]},
    {"name": "Pedro", "grades": [3.0, 4.0, 2.5]},
    {"name": "Sofia", "grades": [7.0, 7.5, 8.0]},
]

# Function to calculate average
def average(grades):
    return sum(grades) / len(grades)

# Function to determine pass/fail
def get_status(avg):
    if avg >= 5.0:
        return "PASS"
    else:
        return "FAIL"

passed = 0
failed = 0

for student in students:
    avg = round(average(student["grades"]), 1)
    status = get_status(avg)

    print(f"{student['name']}: {avg} -> {status}")

    if status == "PASS":
        passed += 1
    else:
        failed += 1

print(f"\nResults: {passed} passed, {failed} failed")
