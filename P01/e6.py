# en el ejercicio 9 que tenemos que hacer lo del readfasta no devolvemos nada, lo "guardamos" en lo d strbases (tenemos que limpiarlo, es decir, ponerlo todo en un string y quitarle la primera linea)
from Seq1 import Seq

print("-----| Practice 1, Exercise 6 |------")

s0 = Seq()
s1 = Seq("ACTGA")
s2 = Seq("Invalid")

print(f"Sequence 0: (Length: {len(s0)}) {s0}")
print(f"  Bases: {s0.count()}")

print(f"Sequence 1: (Length: {len(s1)}) {s1}")
print(f"  Bases: {s1.count()}")

print(f"Sequence 2: (Length: {len(s2)}) {s2}")
print(f"  Bases: {s2.count()}")