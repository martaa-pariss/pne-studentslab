#Given the following string: dna = "ATGCGATCGATCGATCGATCGA"
#Write a program that prints:
    #The total length of the string
    #The first 5 characters
    #The last 3 characters
    #The string converted to lowercase
    #How many times the substring "ATC" appears
    #The string with all occurrences of "T" replaced by "U" (DNA to RNA transcription)


seq = "ATGCGATCGATCGATCGATCGA"
print("The length of the sequence is", len(seq), "bases")
first_five_ch = seq[0:5]
last_three_ch = seq[-3:]
lower_case_seq = seq.lower()
find_ATC = seq.count("ATC")
from_DNA_to_RNA = seq.replace("T", "U")

print("The first five characters of the sequence are", first_five_ch)
print("The last three characters of the sequence are", last_three_ch)
print("The lower-case characters of the sequence are", lower_case_seq)
print("The number of times that appers the substracting ATC is", find_ATC)
print("The sequence replacing Ts by Us is", from_DNA_to_RNA)



