from pathlib import Path
FILENAME = "Sequencess/RNU6_269P.file"
file_contents = Path(FILENAME).read_text()
header = file_contents.split("\n")[0]
print(header)