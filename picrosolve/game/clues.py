from collections.abc import Sequence

class Clue(object):
    def __init__(self, length):
        self._length = length
        self._sequence = None

    @property
    def sequence(self):
        return self._sequence

    @property
    def assign_to_sequence(self, sequence):
        # TODO - check sequence length, and that sequence isn't already filled
        pass

    @property
    def length(self):
        return self._length

    def __str__(self):
        return str(self.length)

    __repr__ = __str__

class ClueList(Sequence):
    def __init__(self, init=[]):
        self.sequence = init

    def __getitem__(self, k):
        if isinstance(k, slice):
            return ClueList(self.sequence[k])
        else:
            return self.sequence[k]

    def __len__(self):
        return len(self.sequence)

    @property
    def minimum_size(self):
        # sum of each clue, plus one for a space between each one
        return self.clue_sum + len(self) - 1

    @property
    def clue_sum(self):
        return sum([clue.length for clue in self])

    @property
    def largest_clue(self):
        return max([clue.length for clue in self])

    def __str__(self):
        return str(self.sequence)
