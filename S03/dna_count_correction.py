def count_bases(seq):
    bases = {"A": 0, "C": 0, "G": 0, "T": 0}
    for base in seq:
        if base in bases:
            bases[base] += 1

    return bases

def main():
    seq = input("enter a sequence: ")
    print("Total length:", len(seq))

    result = count_bases(seq)

    for base, count in result.items():
        print(f'{base}:{count}')

if __name__ == "__main__":
    main() #podemos poner aqui la funcion definida de main y ya, (pero sin poner lo de def main())

#despues de haber escrito lo del __name__ ahora podemoss poner "from dna_count import count_bases" y de esta manera
#podemos usar funciones de unos documentos en otros