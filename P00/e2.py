from P00.Seq0 import seq_read_fasta

#name = input("Enter the full name of the file (make sure )")
    #se podria poner un input pero a la hora de poner lo d "seq_read_fasta(name)" tendriamos que poner f strings creo

names = ["U5", "RNU6_269P", "FXN", "FRAT1", "ADA"]
print("-----Exercice 2-----")
for gene in names:
    full_seq = seq_read_fasta(gene + "(2).file")
    print(f"\n the gene {gene} printed as a single string looks like: \n")
    print(full_seq)