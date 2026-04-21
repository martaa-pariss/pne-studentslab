import json
import termcolor
from pathlib import Path

# -- Read the json file
jsonstring = Path("people-e1.json").read_text()

# Ahora es una lista de personas
people = json.loads(jsonstring)

for person in people:
    print()
    termcolor.cprint("Name: ", 'green', end="")
    print(person['Name'])

    termcolor.cprint("Age: ", 'green', end="")
    print(person['age'])

    phoneNumbers = person['phoneNumber']

    termcolor.cprint("Phone numbers: ", 'green', end='')
    print(len(phoneNumbers))


    for i, dictnum in enumerate(phoneNumbers):
        termcolor.cprint("  Phone " + str(i + 1) + ": ", 'blue')

        termcolor.cprint("\t- Type: ", 'red', end='')
        print(dictnum['type'])

        termcolor.cprint("\t- Number: ", 'red', end='')
        print(dictnum['number'])