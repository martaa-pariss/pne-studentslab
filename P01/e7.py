from Seq1 import Seq

print("-----| Practice 1, Exercise 7 |------")

# Crear secuencias
s0 = Seq()            # nula
s1 = Seq("ACTGA")     # válida
s2 = Seq("Invalid")   # inválida

# Secuencia 0
print(f"Sequence 0: (Length: {len(s0)}) {s0}")
print(f"  Bases: {s0.count()}")
print(f"  Rev:   {s0.reverse()}")

# Secuencia 1
print(f"Sequence 1: (Length: {len(s1)}) {s1}")
print(f"  Bases: {s1.count()}")
print(f"  Rev:   {s1.reverse()}")

# Secuencia 2
print(f"Sequence 2: (Length: {len(s2)}) {s2}")
print(f"  Bases: {s2.count()}")
print(f"  Rev:   {s2.reverse()}")