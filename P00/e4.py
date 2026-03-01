from P00.Seq0 import *

names = ["U5", "RNU6_269P", "FXN", "FRAT1", "ADA"]
print("-----Exercice 4-----")
for gene in names:
    full_seq = seq_read_fasta(gene + "(2).file")
    print(f"\n for the gene {gene} \n")
    print(seq_count_base(full_seq, "A"), "\n", seq_count_base(full_seq, "C"), "\n", seq_count_base(full_seq, "G"), "\n", seq_count_base(full_seq, "T"))