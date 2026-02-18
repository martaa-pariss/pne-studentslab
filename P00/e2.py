from P00.Seq0 import seq_read_fasta

#name = input("Enter the full name of the file (make sure )")
    #se podria poner un input pero a la hora de poner lo d "seq_read_fasta(name)" tendriamos que poner f strings creo
name = ("RNU6_269P(2).file")
full_seq = seq_read_fasta(name)
print("the file seq named", name, "printed as a single string looks like:", "\n", full_seq)