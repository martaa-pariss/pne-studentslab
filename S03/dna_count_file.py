
def count_bases(lis):
    nseq = 0
    for s in lis:
        nseq += 1
        count = 0
        A = 0
        C = 0
        G = 0
        T = 0
        for b in s:
            count += 1
            if b == "A":
                A += 1
            elif b == "C":
                C += 1
            elif b == "G":
                G += 1
            elif b == "T":
                T += 1
        r = print("The total number of As:", A, "The total number of Cs:", C, "The total number of Gs:", G, "The total number of Ts:", T, )
    r2 = print("The number of sequences loaded is", nseq)
    return r, r2

lista = ["AGTACACTGGT", "ACCAGTGTACT", "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"]

c = count_bases(lista)
print(c)



