from abc import ABC, abstractmethod


class DayStrategy(ABC):

    @abstractmethod
    def solve(self) -> None:
        """ The main function to solve the task. """
        pass

    @abstractmethod
    def process_input(self, input_path: str):
        """ Process the input. """
        pass

    @staticmethod
    def read_input(input_path: str) -> list:
        with open(input_path, 'r') as input:
            # Remove the new line char
            return [line.rstrip() for line in input.readlines()]