from Seq1 import Seq

print("-----| Practice 1, Exercise 5 |------")

s0 = Seq()
s1 = Seq("ACTGA")
s2 = Seq("Invalid")

print(f"Sequence 0: (Length: {len(s0)}) {s0}")
print(f"  A: {s0.count_base('A')},   C: {s0.count_base('C')},   T: {s0.count_base('T')},   G: {s0.count_base('G')}")

print(f"Sequence 1: (Length: {len(s1)}) {s1}")
print(f"  A: {s1.count_base('A')},   C: {s1.count_base('C')},   T: {s1.count_base('T')},   G: {s1.count_base('G')}")

print(f"Sequence 2: (Length: {len(s2)}) ERROR")
print(f"  A: {s2.count_base('A')},   C: {s2.count_base('C')},   T: {s2.count_base('T')},   G: {s2.count_base('G')}")