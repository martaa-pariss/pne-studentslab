from pathlib import Path
FILENAME = "Sequencess/RNU6_269P.file"
file_contents = Path(FILENAME).read_text()
headerless = file_contents.split("\n")[1:]
print("\n".join(headerless))
