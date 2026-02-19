from P00.Seq0 import * #con el asterisco estamos importando todas las funciones de Seq0

names = ["U5", "RNU6_269P", "FXN", "FRAT1", "ADA"]
print("-----Exercice 3-----")
for gene in names:
    full_seq = seq_read_fasta(gene + "(2).file")
    print(f"\n for the gene {gene}")
    print("-> Length =", seq_len(full_seq))