from __future__ import annotations
from daystrategy import DayStrategy
from dataclasses import dataclass, field
from typing import Callable, Union
import re
import math


class Day11(DayStrategy):
    def __init__(self):
        pass

    def solve(self) -> None:
        """ The main function to solve the task. """
        monkeys = self.process_input(r'day11/input.txt')

        print(f'The level of monkey business is: {self.solve_monkeys(monkeys.copy(), 20, self.divide_worry_level, 3)}')  # --Part One--

        prod_divisors = math.prod([monkey.test_divisible for monkey in monkeys.values()])

        print(f'The level of monkey business is: {self.solve_monkeys(monkeys.copy(), 10_000, self.modulo_worry_level, prod_divisors)}')  # --Part Two--

    def solve_monkeys(self, monkeys: dict[int, Monkey], num_of_turns: int, worry_calculator: Callable, amount: int) -> int:
        for _ in range(num_of_turns):
            for monkey in monkeys.values():
                for item in monkey.items.copy():
                    new_worry_level = monkey.operation(item)
                    new_worry_level = worry_calculator(new_worry_level, amount)

                    throw_id = monkey.test(new_worry_level)
                    monkeys[throw_id].add_item(new_worry_level)
                    monkey.items.remove(item)

        inspections = [x.inspect_count for x in monkeys.values()]
        inspections.sort(reverse=True)

        return inspections[0] * inspections[1]

    @staticmethod
    def divide_worry_level(worry_level: int, amount: int) -> int:
        # Fine for small number of calculations but not scalable at all.
        return worry_level // amount

    @staticmethod
    def modulo_worry_level(worry_level: int, amount: int) -> int:
        return worry_level % amount

    def process_input(self, input_path: str) -> dict[int, Monkey]:
        monkeys = {}
        monkey = Monkey()

        for line in self.read_input(input_path):
            if not line:
                monkeys[monkey.id] = monkey
                monkey = Monkey()

                continue

            if "Monkey" in line:
                # Get monkey id
                monkey.id = self.extract_numbers_from_text(line, True)
            elif "Operation:" in line:
                monkey.operation = eval(f'lambda old:{line.split("=")[-1]}')
            elif "Starting items:" in line:
                monkey.items = self.extract_numbers_from_text(line)
            elif "Test: divisible by" in line:
                monkey.test_divisible = self.extract_numbers_from_text(line, True)
            elif "If true: throw to monkey" in line:
                monkey.monkey_id_if_true = self.extract_numbers_from_text(line, True)
            elif "If false: throw to monkey" in line:
                monkey.monkey_id_if_false = self.extract_numbers_from_text(line, True)
        else:
            monkeys[monkey.id] = monkey

        return monkeys

    @staticmethod
    def extract_numbers_from_text(text: str, return_first=False) -> Union[int, list[int]]:
        numbers = [int(x) for x in re.findall(r'\d+', text)]
        return numbers if not return_first else numbers[0]


@dataclass
class Monkey:
    id: int = -1
    items: list[int] = field(default_factory=list)
    operation: Callable = None
    test_divisible: int = -1
    monkey_id_if_true: int = -1
    monkey_id_if_false: int = -1

    inspect_count: int = 0

    def test(self, worry_level: int) -> int:
        self.inspect_count += 1

        return self.monkey_id_if_true if worry_level % self.test_divisible == 0 else self.monkey_id_if_false

    def add_item(self, item: int) -> None:
        self.items.append(item)
