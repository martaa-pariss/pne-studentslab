from Seq1 import Seq

print("-----| Practice 1, Exercise 9 |------")

genes = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]
FOLDER = "sequences/"

for gene in genes:

    print(f"\nGene: {gene}")

    filename = FOLDER + gene + ".file"

    s = Seq()
    s.read_fasta(filename)

    print(f"Sequence : (Length: {len(s)}) {s}")
    print(f"  Bases: {s.count()}")
    print(f"  Rev:   {s.reverse()}")
    print(f"  Comp:  {s.complement()}")
