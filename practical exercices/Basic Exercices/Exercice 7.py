student1 = {
    "name": "Carlos",
    "age": 22,
    "subjects": ["PNE", "Networks", "Databases"],
    "grades": {"PNE": 8.5, "Networks": 7.0, "Databases": 9.2}
}

name = student1["name"]
print("The name of the student is:", name)
n_subjects = len(student1["subjects"])
print("Number of subjects:", n_subjects)

if "PNE" in student1["subjects"]:
    value = True
    print("The student is enrolled in pne")
else:
    print("The student is not enrolled in pne")

for subject in student1["subjects"]:
    if subject == "Databases":
        print("Databases grade:", student1["grades"]["Databases"])

grades_avg = 0
for subject, grade in student1["subjects"]:
    grades_avg += grade
grades_avg = round(grades_avg / len(subjects), 2)
print("Student's average grade is:", grades_avg)


#########################################################################################
#ben fet
student = {
    "name": "Carlos",
    "age": 22,
    "subjects": ["PNE", "Networks", "Databases"],
    "grades": {"PNE": 8.5, "Networks": 7.0, "Databases": 9.2}
}
print("Name:", student["name"])
num_subjects = len(student["subjects"])
print("Number of subjects:", num_subjects)

enrolled_pne = "PNE" in student["subjects"]
print("Enrolled in PNE:", enrolled_pne)

databases_grade = student["grades"]["Databases"]
print("Databases grade:", databases_grade)

#AVERAGE
grades_values = student["grades"].values()
average = round(sum(grades_values) / len(grades_values), 2)
print("Average grade:", average)

#TAULA ASSIGNATURES EN NOTES
print("Subject grades:")
for subject, grade in student["grades"].items():
    print(" ", subject + ":", grade)
