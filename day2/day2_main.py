from daystrategy import DayStrategy
from typing import Callable

class HandShape:
    ROCK = 'ROCK'
    PAPER = 'PAPER'
    SCISSORS = 'SCISSORS'


class Day2(DayStrategy):
    def __init__(self) -> None:
        self.hand_shape_map = {'A': HandShape.ROCK, 'B': HandShape.PAPER, 'C': HandShape.SCISSORS, 'X': HandShape.ROCK, 'Y': HandShape.PAPER, 'Z': HandShape.SCISSORS}
        self.hand_shapes = ['ROCK', 'PAPER', 'SCISSORS']
        self.hand_shape_points = [1, 2, 3]

    def solve(self) -> None:
        """ The main function to solve the task. """
        moves = self.process_input(r'day2\input.txt')
        # self.play_game(moves, self.assumed_score_strategy)
        self.play_game(moves, self.correct_score_strategy)

    def process_input(self, input_path: str):
        """ Process the input. """
        moves = []

        for line in self.read_input(input_path):
            pairs = line.strip().split()

            moves.append(pairs)

        return moves

    @staticmethod
    def play_game(moves: list[list[str]], score_strategy: Callable) -> None:
        total_score = 0

        for opponent, player in moves:
            total_score += score_strategy(opponent, player)

        print(f'Your total score is: {total_score}')

    def assumed_score_strategy(self, opponent: str, player: str) -> int:
        opponent_index = self.hand_shapes.index(self.hand_shape_map[opponent])
        player_index = self.hand_shapes.index(self.hand_shape_map[player])

        points = 0

        print('========================')
        print(f'{opponent} vs. {player}')

        if opponent_index == player_index:
            # Draw
            print("It's a DRAW!")
            points += 3
        elif player_index == ((opponent_index + 1) % 3):
            # Player wins
            print("Player WINS!")
            points += 6
        else:
            print("Player LOOSES!")

        print(f'Round score: {points + self.hand_shape_points[player_index]}')
        print('========================')

        return points + self.hand_shape_points[player_index]

    def correct_score_strategy(self, opponent: str, player: str) -> int:
        opponent_index = self.hand_shapes.index(self.hand_shape_map[opponent])

        print('========================')
        print(f'{opponent} vs. {player}')
        points = 0

        if player == 'X':
            # The player needs to loose
            print("Player LOOSES!")
            points += self.hand_shape_points[((opponent_index - 1) % 3)]
        elif player == 'Y':
            # The round needs to end in draw
            print("It's a DRAW!")
            points += 3 + self.hand_shape_points[opponent_index]
        elif player == 'Z':
            # The player needs to win
            print("Player WINS!")
            points += 6 + self.hand_shape_points[((opponent_index + 1) % 3)]

        print(f'Round score: {points}')
        print('========================')

        return points