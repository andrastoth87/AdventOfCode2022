from __future__ import annotations
from daystrategy import DayStrategy
from dataclasses import dataclass, astuple


class Day9(DayStrategy):
    def __init__(self):
        self.KNOT_COUNT = 10

        # HEAD will be knots_positions[0], tail will be knots_positions[-1]
        self.knots_positions: list[IntVector2] = []
        self.visited_positions: dict[tuple[int, int], int] = {}

    def solve(self) -> None:
        """ The main function to solve the task. """
        moves = self.process_input(r'day9/input.txt')

        self.initialize_knots()

        self.process_moves(moves)

        print(f'Number of positions the tail visited at least once: {len(self.visited_positions)}')

    def process_input(self, input_path: str):
        moves = []

        directions = {'U': IntVector2(0, 1), 'D': IntVector2(0, -1), 'L': IntVector2(-1, 0), 'R': IntVector2(1, 0)}

        for line in self.read_input(input_path):
            direction, step = line.split()

            moves.append([directions.get(direction), int(step)])

        return moves

    def initialize_knots(self) -> None:
        for _ in range(self.KNOT_COUNT):
            self.knots_positions.append(IntVector2(0, 0))

    def process_moves(self, moves: list[list[IntVector2, int]]) -> None:
        self.mark_tail_position()

        for move in moves:
            direction, step = move

            for _ in range(step):
                self.move_head(direction)
                self.move_knots()

                self.mark_tail_position()

    def move_head(self, direction: IntVector2) -> None:
        self.knots_positions[0] += direction

    def move_knots(self):
        for i in range(1, self.KNOT_COUNT):
            x_distance = self.knots_positions[i - 1].x - self.knots_positions[i].x
            y_distance = self.knots_positions[i - 1].y - self.knots_positions[i].y

            if abs(x_distance) > 1 or abs(y_distance) > 1:
                self.knots_positions[i].x += self.sign(x_distance)
                self.knots_positions[i].y += self.sign(y_distance)

    def mark_tail_position(self) -> None:
        try:
            self.visited_positions[astuple(self.knots_positions[-1])] += 1
        except KeyError:
            self.visited_positions[astuple(self.knots_positions[-1])] = 1

    @staticmethod
    def sign(x: int) -> int:
        return (x > 0) - (x < 0)


@dataclass()
class IntVector2:
    x: int = 0
    y: int = 0

    def __add__(self, other: IntVector2):
        return IntVector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: IntVector2):
        return IntVector2(self.x - other.x, self.y - other.y)
