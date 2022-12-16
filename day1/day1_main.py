from daystrategy import DayStrategy


class Day1(DayStrategy):
    def __init__(self) -> None:
        pass

    def solve(self) -> None:
        """ The main function to solve the task. """
        elf_calories = self.process_input(r'day1\input.txt')

        self.get_top_calories(elf_calories, 1)
        self.get_top_calories(elf_calories, 3)

    def process_input(self, input_path: str) -> dict[int, int]:
        """ Process the input. """
        elf_calories = {}
        elf_counter = 1

        calories = []

        for line in self.read_input(input_path):
            try:
                calories.append(int(line))
            except ValueError:
                elf_calories[elf_counter] = sum(calories)
                calories.clear()
                elf_counter += 1

        return elf_calories

    @staticmethod
    def get_top_calories(elf_calories: dict[int, int], top_count: int = 1) -> None:
        """ Returns the top number of elfs with the highest calories"""
        top_elf_calories = dict(sorted(elf_calories.items(), key=lambda x: x[1], reverse=True)[:max(1, top_count)])

        for key, value in top_elf_calories.items():
            print(f'Elf #{key} has {value} of calories.')

        if top_count > 1:
            print(f'\nThe sum of calories is: {sum(top_elf_calories.values())}\n')
        else:
            print('\n')



