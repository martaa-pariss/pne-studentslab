# CORRECCION
lines = ["AGTACACTGGT", "ACCAGTGTACT", "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"]

#podemos abrir el documento con este primer metodo, con el f = open...; de esta manera estamos haciendo uso de muchas lineas
f = open("dna.txt", "r") #de esta manera abrimos un documento sin usar pandas (open es una funcion de python)
#here we put de code
lines = f.readlines()
print("From file:", lines)
f.close()

#de esta manera podemos tambien abrir el documento pero con muchas menos lineas
with open("dna.txt", "r") as f:
    lines = f.readlines()

total_number = 0
bases = {"A": 0, "C": 0, "G": 0, "T": 0}
for seq in lines:
    seq = seq.strip() #this function remove spaces and newline characters at the end of the string
    total_number += len(seq)
    for base in seq:
        if base in bases:
            bases[base] += 1

print("Total number of bases", total_number)

#for base, count in bases.items():