class Seq:
    """A class for representing sequences"""

    def __init__(self, strbases=None):
        valid_bases = ['A', 'C', 'G', 'T']

        self.strbases = None
        self.invalid = False

        if strbases is None:
            print("NULL sequence created")
        else:
            for base in strbases:
                if base not in valid_bases:
                    print("INVALID sequence!")
                    self.invalid = True
                    return

            self.strbases = strbases
            print("New sequence created!")

    def __str__(self):
        if self.invalid:
            return "ERROR"
        if self.strbases is None:
            return "NULL"
        return self.strbases

    def __len__(self):
        if self.strbases is None or self.invalid:
            return 0
        return len(self.strbases)

    def len(self):
        return len(self.strbases)

    def count_base(self, base):
        if self.strbases is None or self.invalid:
            return 0
        return self.strbases.count(base)

    def count(self):  #cuenta el numero de base por cada base
        bases_dict = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
        if self.strbases is None or self.invalid:
            return bases_dict
        for base in self.strbases:
            bases_dict[base] += 1
        return bases_dict

    def percentage(self):
        bases_dict = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

        if self.strbases is None or self.invalid:
            return bases_dict

        total = len(self.strbases)

        counts = self.count()

        for base in bases_dict:
            bases_dict[base] = (counts[base] / total) * 100

        return bases_dict

    def max_base(self):
        percentages = self.percentage()

        if self.strbases is None or self.invalid:
            return None

        max_base = None
        max_value = 0

        for base in percentages:
            value = percentages[base]

            if max_base is None:
                max_base = base
                max_value = value
            elif value > max_value:
                max_base = base
                max_value = value

        return max_base, max_value

    def reverse(self):
        if self.strbases is None or self.invalid:
            return str(self)
        return self.strbases[::-1]

    def complement(self):
        if self.strbases is None or self.invalid:
            return str(self)
        comp_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return ''.join([comp_dict[base] for base in self.strbases])

    def read_fasta(self, filename):
        sequence = ""
        with open(filename, "r") as f:
            for line in f:
                if line.startswith(">"):
                    continue
                sequence += line.strip()

        self.strbases = sequence

