class Seq:
    """A class for representing sequences"""

    def __init__(self, strbases):
        valid_bases = ['A', 'C', 'G', 'T']

        for base in strbases:
            if base not in valid_bases:
                self.strbases = "ERROR"
                print("ERROR!!")
                return

        self.strbases = strbases
        print("New sequence created!")

    def __str__(self):
        return self.strbases

    def len(self):
        """Calculate the length of the sequence"""
        return len(self.strbases)


def print_seqs(seq_list):
    for index, seq in enumerate(seq_list):
        print(f"Sequence {index}: (Length: {seq.len()}) {seq}")


def generate_seqs(pattern, number):
    seq_list = []

    for i in range(number):
        new_sequence = pattern * (i + 1)
        seq_obj = Seq(new_sequence)
        seq_list.append(seq_obj)

    return seq_list

seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

print("List 1:")
print_seqs(seq_list1)

print()
print("List 2:")
print_seqs(seq_list2)
