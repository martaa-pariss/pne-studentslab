from P00.Seq0 import *

names = ["U5", "RNU6_269P", "FXN", "FRAT1", "ADA"]
print("-----Exercice 8-----")
for gene in names:
    full_seq = seq_read_fasta(gene + "(2).file")
    print(f"\n for the gene {gene} \n")
    print("most common base in", gene, "is:", most_common_base(full_seq))