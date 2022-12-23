from daystrategy import DayStrategy
from typing import Callable


class Day8(DayStrategy):
    def __init__(self):
        self.width = 0
        self.height = 0

    def solve(self) -> None:
        """ The main function to solve the task. """
        forest = self.process_input(r'day8/input.txt')
        self.width, self.height = self.get_forest_size(forest)

        print(f'Number of trees that are visible from outside the grid: {sum(self.calculate_visible_trees(forest, self.calculate_tree_visible_from_outside))}')  # --Part One--
        print(f'Highest scenic score possible for any tree: {max(self.calculate_visible_trees(forest, self.calculate_tree_scenic_score))}')  # --Part Two--

    def process_input(self, input_path: str):
        forest = []

        for line in self.read_input(input_path):
            forest.append([int(x) for x in line])

        return forest

    @staticmethod
    def get_forest_size(forest: list[list[int]]) -> tuple:
        x = max(map(len, forest))  # returns length of the widest sublist
        y = len(forest)

        return x, y

    def calculate_visible_trees(self, forest: list[list[int]], score_strategy: Callable) -> list[int]:
        score = []

        for x in range(self.width):
            for y in range(self.height):
                tree = forest[y][x]
                horizontal_tree_line = forest[y]
                vertical_tree_line = [sublist[x] for sublist in forest]

                score.append(score_strategy(x, y, tree, horizontal_tree_line, vertical_tree_line))

        return score

    def calculate_tree_visible_from_outside(self, x: int, y: int, current_tree: int, horizontal_tree_line: list[int], vertical_tree_line: list[int]):
        tree_lines = horizontal_tree_line[:x:-1], horizontal_tree_line[:x], vertical_tree_line[:y], vertical_tree_line[:y:-1]
        for tree_line in tree_lines:
            if self.is_visible(current_tree, tree_line):
                return 1

        return 0

    @staticmethod
    def is_visible(current_tree: int, tree_line: list[int]) -> bool:
        for tree in tree_line:
            if tree >= current_tree:
                return False

        return True

    def calculate_tree_scenic_score(self, x: int, y: int, current_tree: int, horizontal_tree_line: list[int], vertical_tree_line: list[int]):
        # horizontal_tree_line[x+1:]  # Horizontal from tree to right
        # horizontal_tree_line[x::-1][1:]  # Horizontal from tree to left
        # vertical_tree_line[y+1:]  # Vertical from tree to down
        # vertical_tree_line[y::-1][1:]  # Vertical from tree to up

        tree_lines = [horizontal_tree_line[x+1:], horizontal_tree_line[x::-1][1:], vertical_tree_line[y+1:], vertical_tree_line[y::-1][1:]]
        tree_score = 1

        for tree_line in tree_lines:
            tree_score *= self.get_viewing_range(current_tree, tree_line)

        return tree_score

    @staticmethod
    def get_viewing_range(current_tree: int, tree_line: list[int]) -> int:
        view_range = 0

        for tree in tree_line:
            view_range += 1

            if tree >= current_tree:
                return view_range

        return view_range
