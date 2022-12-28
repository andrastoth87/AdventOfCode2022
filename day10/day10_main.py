from daystrategy import DayStrategy
from typing import Callable
from textwrap import wrap


class Day10(DayStrategy):
    def __init__(self):
        pass

    def solve(self) -> None:
        """ The main function to solve the task. """
        commands = self.process_input(r'day10/input.txt')

        # print(f'The sum of the six signal strengths: {sum(self.process_commands(commands, self.try_calculate_signal_strength))}')  # --Part One--

        crt = self.process_commands(commands, self.get_pixel_type)

        self.draw_crt(crt)

    def process_input(self, input_path: str):
        return self.read_input(input_path)

    @staticmethod
    def draw_crt(crt: list[str]):
        crt_width = 40
        crt = wrap(''.join(crt), crt_width)

        for line in crt:
            print(line)

    @staticmethod
    def process_commands(commands: list[str], signal_processor: Callable) -> list:
        x = 1
        current_cycle = 0
        signal = []

        for line in commands:
            if not line:
                continue

            command, *value = line.split()
            signal.append(signal_processor(current_cycle, x))

            current_cycle += 1

            if command == 'addx':
                signal.append(signal_processor(current_cycle, x))

                current_cycle += 1

                x += int(value[0])

        return signal

    @staticmethod
    def try_calculate_signal_strength(current_cycle: int, x: int) -> int:
        cycles = [20, 60, 100, 140, 180, 220]

        if current_cycle in cycles:
            return current_cycle * x

        return 0

    @staticmethod
    def get_pixel_type(current_cycle: int, x: int) -> str:
        crt_width = 40

        if x - 1 <= (current_cycle % crt_width) <= x + 1:
            return '#'

        return '.'
