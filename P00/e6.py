from P00.Seq0 import *

names = ["U5", "RNU6_269P", "FXN", "FRAT1", "ADA"]
print("-----Exercice 6-----")
for gene in names:
    full_seq = seq_read_fasta(gene + "(2).file")
    print(f"\n for the gene {gene} \n")
    print("Original sequence:", full_seq,"\n" , "Reverse sequence:", seq_reverse(full_seq))