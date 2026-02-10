#counting bases of a DNA seq
    #we are supposing that the input seqs are correct

seq = input("Enter a sequence: ")
count = 0
A = 0
C = 0
G = 0
T = 0
for b in seq:
    count += 1
    if b == "A":
        A += 1
    elif b == "C":
        C += 1
    elif b == "G":
        G += 1
    elif b == "T":
        T += 1

print("Number of As: ", A)
print("Number of Cs: ", C)
print("Number of Gs: ", G)
print("Number of Ts: ", T)
print("total number of bases:", count)

