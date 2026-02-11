words = ["Python", "is", "a", "programming", "language"]

#a)
def count_characters(word):
    count = 0
    for letter in word:
        count += 1
    return count

for word in words:
    print(word, "->", count_characters(word), "characters")

#b)
starting_nuber = n = 1
while n < 1000:
    print(n)
    n += n * 2
