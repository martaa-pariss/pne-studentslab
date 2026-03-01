class Seq:
    """A class for representing sequences"""

    def __init__(self, strbases):
        valid_bases = ['A', 'C', 'G', 'T']

        for base in strbases:
            if base not in valid_bases:
                self.strbases = "ERROR"
                print("INCORRECT Sequence detected")
                return

        self.strbases = strbases
        print("New sequence created!")

    def __str__(self):
        return self.strbases

    def len(self):
        """Calculate the length of the sequence"""
        return len(self.strbases)


s1 = Seq("ACCTGC")
s2 = Seq("Hello? Am I a valid sequence?")
print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")
