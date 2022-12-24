from daystrategy import DayStrategy
from day1.day1_main import Day1
from day2.day2_main import Day2
from day3.day3_main import Day3
from day4.day4_main import Day4
from day5.day5_main import Day5
from day6.day6_main import Day6
from day7.day7_main import Day7
from day8.day8_main import Day8
from day9.day9_main import Day9


def main(strategy: DayStrategy) -> None:
    strategy.solve()


if __name__ == '__main__':
    main(Day9())
