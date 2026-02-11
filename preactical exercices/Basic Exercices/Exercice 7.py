student = {
    "name": "Carlos",
    "age": 22,
    "subjects": ["PNE", "Networks", "Databases"],
    "grades": {"PNE": 8.5, "Networks": 7.0, "Databases": 9.2}
}

for key, value in student.items():
    if key == "name":
        print("The name of the student is:", value)
    elif key == "subjects":
        number_of_subjects = len(value)
        for subject in value["subjects"]:
            if "PNE" in subject:
                print("The student has chosen PNE as a subject")
    elif key == "grades":
        list_of_grades = [""]
        for k, value in key.items():
            list_of_grades.append(value)
            if k == "Databases":
                print("The grade of the student in the subject of databases is", value)
        average_grade = sum(list_of_grades) / len(list_of_grades)
        print("The average grade of the student is:", round(average_grade))
        print(key)

