def seq_ping():
    return "ok"

def seq_read_fasta(filename):
    from pathlib import Path
    FILENAME = filename
    file_contents = Path(FILENAME).read_text()
    header = file_contents.split("\n")[1:] #aqui se guarda toda la secuancia menos el header
    final = "".join(header) #aqui se une toda la secuencia en un solo  string
    return final


def seq_len(seq):
    number = len(seq)
    return number


def seq_count_base(seq, base):
    s_count = 0
    for b in seq:
        if base == b:
            s_count += 1
    output = (base,":", s_count)
    return output

def seq_count(seq):
    A = 0
    C = 0
    G = 0
    T = 0
    for base in seq:
        if base == "A":
            A += 1
        elif base == "C":
            C += 1
        elif base == "G":
            G += 1
        elif base == "T":
            T += 1
    output = {'A': A, 'T': T, 'C': C, 'G': G}
    return output

def seq_reverse(seq):
    reversed_seq = seq[::-1]
    return reversed_seq


def seq_complement(seq):
    comp_seq = ""
    for base in seq:
        if base == "A":
            comp_seq += "T"
        elif base == "C":
            comp_seq += "G"
        elif base == "G":
            comp_seq += "C"
        elif base == "T":
            comp_seq += "A"
    return comp_seq

def most_common_base(seq):
    A = 0
    C = 0
    G = 0
    T = 0
    for base in seq:
        if base == "A":
            A += 1
        elif base == "C":
            C += 1
        elif base == "G":
            G += 1
        elif base == "T":
            T += 1
    if A > C and A > G and A > T:
        output = "A"
    elif C > A and C > G and C > T:
        output = "C"
    elif G > C and G > A and G > T:
        output = "G"
    elif T > C and T > G and T > A:
        output = "T"
    return output


sequ = "GGGGATTTCCAGTCCGAAATTCCTGAGCCCACAATAAAGAAGGGCTGATCTCAAACAGCCTGAGCCTGGTGTCCTAATGGAATGA"
print("For the sequence RNU6_269P -> Length =", seq_len(sequ))

print("------Exercice 4------")
print("Gene RNU6_269P:", "\n", seq_count_base(sequ, "A"), "\n", seq_count_base(sequ, "C"), "\n", seq_count_base(sequ, "G"), "\n", seq_count_base(sequ, "T") )

print("------Exercice 5------")
print(seq_count(sequ))

print("------Exercice 6------")
print("Original sequence:", sequ,"\n" , "Reverse sequence:", seq_reverse(sequ))

print("------Exercice 7------")
print("Original sequence:", sequ,"\n" , "Complementary sequence:", seq_complement(sequ))

print("------Exercice 8------")
print("RNU6_269P's most common base is:", most_common_base(sequ))