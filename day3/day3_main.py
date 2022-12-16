from daystrategy import DayStrategy
import string
from typing import Callable


class Day3(DayStrategy):
    def __init__(self):
        self.priority_list = list(string.ascii_lowercase) + list(string.ascii_uppercase)

    def solve(self) -> None:
        """ The main function to solve the task. """
        rucksack_contents = self.process_input(r'day3/input.txt')
        # self.calculate_common_sums(rucksack_contents, self.single_rucksack_strategy)
        self.calculate_common_sums(rucksack_contents, self.group_rucksack_strategy)

    def process_input(self, input_path: str):
        return self.read_input(input_path)

    def calculate_common_sums(self, rucksack_contents: list[list[str]], rucksack_strategy: Callable) -> None:
        """ Solution for part 1 """
        priorites_sum = 0

        for contents in rucksack_strategy(rucksack_contents):
            common_elements = self.get_common_elements(contents)

            for item in common_elements:
                priorites_sum += self.get_item_priority(item)

        print(f'The sum of priorities for common items: {priorites_sum}')

    @staticmethod
    def single_rucksack_strategy(rucksack_contents: list[list[str]]):
        for contents in rucksack_contents:
            content_count = len(contents) // 2

            yield [contents[:content_count], contents[content_count:]]

    @staticmethod
    def group_rucksack_strategy(rucksack_contents: list[list[str]]):
        for i in range(0, len(rucksack_contents), 3):
            yield [rucksack_contents[i], rucksack_contents[i + 1], rucksack_contents[i + 2]]


    @staticmethod
    def get_common_elements(contents: list[list[str]]) -> list[str]:
        """ Returns the common elements of the supplied lists. """
        if len(contents) < 2:
            return []

        common_items = set(contents[0])

        for contents in contents[1:]:
            common_items.intersection_update(contents)

        return list(common_items)

    def get_item_priority(self, item: str) -> int:
        """ Returns the priority of an item. Priorities start at 1. """
        return self.priority_list.index(item) + 1
