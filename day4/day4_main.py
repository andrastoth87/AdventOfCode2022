from daystrategy import DayStrategy
from dataclasses import dataclass
from typing import Callable

class Day4(DayStrategy):
    def __init__(self):
        pass

    def solve(self) -> None:
        """ The main function to solve the task. """
        sections = self.process_input(r'day4/input.txt')
        # self.find_overlap_count(sections, self.fully_contains_strategy)
        self.find_overlap_count(sections, self.overlaps_strategy)

    def process_input(self, input_path: str):
        sections = []

        for section in self.read_input(input_path):
            section_a, section_b = section.split(',')
            # Create the section pairs and cast everything to int
            sections.append([Section(*[int(x) for x in section_a.split('-')]), Section(*[int(x) for x in section_b.split('-')])])

        return sections

    @staticmethod
    def find_overlap_count(sections, comparer: Callable) -> None:
        overlap_count = 0
        for section_a, section_b in sections:
            overlap_count += int(comparer(section_a, section_b))

        print(f'Overlaps found: {overlap_count}')

    @staticmethod
    def fully_contains_strategy(section_a, section_b) -> bool:
        """ Returns true if one segments is fully contained by another. """
        return (section_a.start >= section_b.start and section_a.end <= section_b.end) or (section_b.start >= section_a.start and section_b.end <= section_a.end)

    @staticmethod
    def overlaps_strategy(section_a, section_b) -> bool:
        """ Returns true if there's some overlap. """
        return not (section_a.end < section_b.start or section_a.start > section_b.end or section_b.end < section_a.start or section_b.start > section_a.end)


@dataclass()
class Section:
    start: int = 0
    end: int = 0
