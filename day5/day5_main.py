from daystrategy import DayStrategy
from dataclasses import dataclass
from typing import Callable
import re

class Day5(DayStrategy):
    def __init__(self):
        self.supply_stack = {}
        self.crate_width = 3
        self.separator_width = 1 #  The number of spaces between the columns of crates

        self.orders = []


    def solve(self) -> None:
        """ The main function to solve the task. """
        self.process_input(r'day5/input.txt')
        # self.execute_orders()
        self.execute_orders(False)
        self.print_last_crates()

    def process_input(self, input_path: str):
        stack_finished = False

        for line in self.read_input(input_path):
            if not stack_finished:
                if not self.add_crate_to_stack(line):
                    stack_finished = True

                    # Reverse the order of the stacks
                    for value in self.supply_stack.values():
                        value.reverse()

            else:
                self.add_order(line)

    def execute_orders(self, rearange: bool = True) -> None:
        for quantity, from_stack, to_stack in self.orders:
            stack = self.supply_stack[from_stack]

            self.supply_stack[from_stack] = stack[:-quantity]

            if rearange:
                self.supply_stack[to_stack] += stack[-quantity:][::-1]  # [::-1] reverses a list

            else:
                self.supply_stack[to_stack] += stack[-quantity:]

    def print_last_crates(self) -> None:
        last_crates = ''

        for i in range(len(self.supply_stack)):
            try:
                last_crates += self.supply_stack.get(i + 1, [])[-1]
            except IndexError:
                pass

        # Remove the [ and ] characters
        last_crates = re.sub('\[|]', '', last_crates)

        print(f'The last crates spell out: {last_crates}')

    def add_crate_to_stack(self, line: str) -> bool:
        """ Adds the crate to the required stack. """
        stack_constructed = True

        matches = re.finditer(r'\[[A-Z]]', line)
        indices = [m.start(0) for m in matches]

        if not indices:
            stack_constructed = False

        for position in indices:
            number_of_separators = position // (self.crate_width + self.separator_width)

            key = ((position - number_of_separators * self.separator_width) // self.crate_width) + 1

            try:
                self.supply_stack[key].append(line[position: position + self.crate_width])
            except KeyError:
                self.supply_stack[key] = []
                self.supply_stack[key].append(line[position: position + self.crate_width])

        return stack_constructed

    def add_order(self, line: str) -> None:
        match = re.match(r'move (\d*) from (\d*) to (\d*)', line)

        if match is None:
            return

        self.orders.append([int(x) for x in match.groups()])