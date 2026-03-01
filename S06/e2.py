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


# Main program
seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]

print_seqs(seq_list)
