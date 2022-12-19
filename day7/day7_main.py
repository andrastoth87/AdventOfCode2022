from __future__ import annotations
from daystrategy import DayStrategy
from dataclasses import dataclass
from typing import Optional
import re


class Day7(DayStrategy):
    def __init__(self):
        pass

    def solve(self) -> None:
        """ The main function to solve the task. """
        input_tree = self.process_input(r'day7/input.txt')

        tree = self.construct_tree(input_tree)
        # print(self.get_content_size(tree))

        sizes = {}

        for dir in tree.get_all_directories():
            sizes[dir.data.name] = self.get_content_size(dir)

        size_sum = 0

        for size in sizes.values():
            if size <= 100000:
                size_sum += size

        print(size_sum)

    def process_input(self, input_path: str):
        return self.read_input(input_path)

    @staticmethod
    def construct_tree(input_tree) -> Node:
        current_node = None
        root = None

        for line in input_tree:
            keyword, *other = line.split()

            # Pad the list because we always want it to contain 2 elements
            other += [''] * (2 - len(other))

            if keyword == '$':
                # It`s a command
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

    @staticmethod
    def get_content_size(node: Node, size=0):
        for child in node.children:
            size += child.get_content_size(child.data.size)

        return size


class Node:
    def __init__(self, parent: Optional[Node], data: Data):
        self.parent: Optional[Node] = parent
        self.children: list[Node] = []
        self.level: int = 0 if parent is None else parent.level + 1
        self.data: Optional[Data] = data

    def get_directory_by_name(self, name: str) -> Node:
        """ Returns the child with a matching name"""
        for child in self.children:
            if child.data.name == name and child.data.data_type == DataType.DIRECTORY:
                return child

        return self

    def get_all_directories(self, directories: list[Node] = []) -> list:
        for child in self.children:
            if child.data.data_type == DataType.DIRECTORY:
                directories.append(child)

            child.get_all_directories(directories)

        return directories

    def get_parent(self) -> Node:
        """ Returns the parent if it`s a child otherwise it will return self. """
        return self.parent if self.parent is not None else self

    def get_content_size(self, size=0):
        for child in self.children:
            size += child.get_content_size(child.data.size)

        return size

    def add_child(self, child: Node):
        self.children.append(child)


class DataType:
    FILE = 'FILE'
    DIRECTORY = 'DIRECTORY'

@dataclass()
class Data:
    name: str
    data_type: str
    size: int = 0


