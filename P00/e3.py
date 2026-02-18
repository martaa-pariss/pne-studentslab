from P00.Seq0 import * #con el asterisco estamos importando todas las funciones de Seq0

#reading and cleaning the sequence
name = "../S04/sequences/RNU6_269P.file"
full_seq = seq_read_fasta(name)

length = seq_len(full_seq)
print(length)