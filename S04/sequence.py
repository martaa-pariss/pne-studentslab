from pathlib import Path
FILENAME = "Sequencess/ADA.file"
file_contents = Path(FILENAME).read_text()
header = file_contents.split("\n")[1:]
final = "".join(header)
number = len(final)

print("The total number of bases in the ADA file is: ", number)