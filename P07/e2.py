genes = {
    "FRAT1": "ENSG00000165879",
    "ADA": "ENSG00000196839",
    "FXN": "ENSG00000165060",
    "RNU6_269P": "ENSG00000206621",
    "MIR633": "ENSG00000207552",
    "TTTY4C": "ENSG00000228658",
    "RBMY2YP": "ENSG00000226374",
    "FGFR3": "ENSG00000068078",
    "KDR": "ENSG00000128052",
    "ANK2": "ENSG00000145362"
}

#no imprimeix be, imprimeix la primera lletra joder
for gene in genes:

    print(f"{gene[0]} --> {gene[1]}")