from daystrategy import DayStrategy


class Day6(DayStrategy):
    def __init__(self):
        pass

    def solve(self) -> None:
        """ The main function to solve the task. """
        sequences = self.process_input(r'day6/input.txt')

        # self.process_sequences(sequences, 4)  # ---Part One---
        self.process_sequences(sequences, 14)  # ---Part Two---

    def process_input(self, input_path: str):
        return self.read_input(input_path)

    def process_sequences(self, sequences: list[str], sample_size: int) -> None:
        for sequence in sequences:
            for i in range(sample_size, len(sequence) + 1, 1):
                if self.is_unique(list(sequence[i-sample_size:i])):
                    print(f'The marker is at: {i}')

                    return

    @staticmethod
    def is_unique(sample: list[str]) -> bool:
        return len(sample) == len(set(sample))