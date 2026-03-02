from Seq1 import Seq

print("-----| Practice 1, Exercise 10 |------")

genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
FOLDER = "sequences/"

for gene in genes:
    s = Seq()
    filename = FOLDER + gene + ".file"
    s.read_fasta(filename)

    bases_dict = s.count()
    most_frequent = max(bases_dict, key=bases_dict.get)

    print(f"Gene {gene}: Most frequent Base: {most_frequent}")