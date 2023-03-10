from __future__ import annotations
from daystrategy import DayStrategy
from dataclasses import dataclass
from typing import Optional


class Day7(DayStrategy):
    def __init__(self):
        # Use _ with numbers for better readability
        self.MAX_AVAILABLE_SPACE = 70_000_000
        self.REQUIRED_SPACE = 30_000_000
        self.MAX_DIRECTORY_SIZE = 100_000

    def solve(self) -> None:
        """ The main function to solve the task. """
        commands = self.process_input(r'day7/input.txt')

        tree = self.construct_tree(commands)
        self.print_tree(tree)

        sizes = []

        for directory in self.get_all_directories(tree, []):
            sizes.append(self.get_content_size(directory))

        print(f'\nSum of size of directories that are at most 100 000: {sum(i for i in sizes if i <= self.MAX_DIRECTORY_SIZE)}')

        used_space = self.get_content_size(tree)
        free_space = self.MAX_AVAILABLE_SPACE - used_space

        smallest_match = next((i for i in sorted(sizes) if free_space + i >= self.REQUIRED_SPACE), None)

        print(f'Smallest directory to delete to free up the required space: {smallest_match}')

    def process_input(self, input_path: str):
        return self.read_input(input_path)

    @staticmethod
    def construct_tree(input_tree) -> Node:
        current_node = None
        root = None

        for line in input_tree:
            keyword, *other = line.split()

            if keyword == '$':
                # It`s a command
                # Pad the list to two elements
                other += [''] * (2 - len(other))

                command, option = other

                if command == 'cd':
                    if option == '..':
                        current_node = current_node.get_parent()
                    else:
                        if current_node is None:
                            current_node = Node(None, Data(name=option, data_type=DataType.DIRECTORY))
                            root = current_node

                        current_node = current_node.get_directory_by_name(option)

            elif keyword == 'dir':
                # It`s a directory
                name, = other
                current_node.add_child(Node(current_node, Data(name=name, data_type=DataType.DIRECTORY, size=0)))

            else:
                # It's a file
                name, = other
                current_node.add_child(Node(current_node, Data(name=name, data_type=DataType.FILE, size=int(keyword))))

        return root

    def print_tree(self, node: Node) -> None:
        print(f'{chr(9) * node.level} - {node.data.name} (dir)')
        for child in node.children:
            if child.data.data_type == DataType.DIRECTORY:
                self.print_tree(child)

                continue

            print(f'{chr(9) * child.level} - {child.data.name} (file, {child.data.size})')

    def get_content_size(self, node: Node, size=0):
        """ Recursively calculates the size of a node and it's children. """
        for child in node.children:
            size += self.get_content_size(child, child.data.size)

        return size

    def get_all_directories(self, node: Node, directories: list[Node]) -> list[Node]:
        """ Recursively returns all the directories of a node and it's children. """
        for child in node.children:
            if child.data.data_type == DataType.DIRECTORY:
                directories.append(child)

            self.get_all_directories(child, directories)

        return directories


class Node:
    def __init__(self, parent: Optional[Node], data: Data):
        self.parent: Optional[Node] = parent
        self.children: list[Node] = []
        self.level: int = 0 if parent is None else parent.level + 1
        self.data: Optional[Data] = data

    def add_child(self, child: Node):
        self.children.append(child)

    def get_parent(self) -> Node:
        """ Returns the parent if it`s a child otherwise it will return self. """
        return self.parent if self.parent is not None else self

    def get_directory_by_name(self, name: str) -> Node:
        """ Returns the child with a matching name"""
        for child in self.children:
            if child.data.name == name and child.data.data_type == DataType.DIRECTORY:
                return child

        return self


class DataType:
    FILE = 'FILE'
    DIRECTORY = 'DIRECTORY'


@dataclass()
class Data:
    name: str
    data_type: str
    size: int = 0


