from day1.day1_main import Day1
from day2.day2_main import Day2
from day3.day3_main import Day3
from day4.day4_main import Day4
from day5.day5_main import Day5

from daystrategy import DayStrategy


def main(strategy: DayStrategy) -> None:
    strategy.solve()


if __name__ == '__main__':
    main(Day5())
