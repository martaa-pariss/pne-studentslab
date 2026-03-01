from Seq1 import Seq
# -- Create a Null sequence
s1 = Seq()

# -- Create a valid sequence
s2 = Seq("ACTGA")

# -- Create an invalid sequence
s3 = Seq("Invalid sequence")


print("-----Practice 1, Exercice 3-----")
print(f"Sequence 1 (Length: {len(s1)}): {s1}")
print(f"Sequence 2 (Length: {len(s2)}): {s2}")
print(f"Sequence 1 (Length: {len(s3)}): {s3}")


#poner los len de cada secuencia; si no es valida o es nula len es 0