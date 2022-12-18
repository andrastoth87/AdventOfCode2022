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
        print(self.get_size_sum(tree))

    def process_input(self, input_path: str):
        return self.read_input(input_path)

    def construct_tree(self, input_tree) -> Node:
        current_node = None
        root = None

        for line in input_tree:
            matches = line.split()

            if matches[0] == '$':
                # It`s a command
                if matches[1] == 'cd':
                    if matches[2] == '..':
                        current_node = current_node.get_parent()
                    else:
                        if current_node is None:
                            current_node = Node(None, Data(name=matches[2], data_type=DataType.DIRECTORY))
                            root = current_node

                        current_node = current_node.get_directory_by_name(matches[2])

            elif matches[0] == 'dir':
                # It`s a directory
                current_node.add_child(Node(current_node, Data(name=matches[1], data_type=DataType.DIRECTORY, size=0)))

            elif matches[0].isdigit():
                # It's a file
                current_node.add_child(Node(current_node, Data(name=matches[1], data_type=DataType.FILE, size=int(matches[0]))))

        return root

    def get_size_sum(self, node: Node, size=0):
        size_sum = size

        for child in node.children:
            size_sum += child.get_size_sum(child.data.size)

        return size_sum


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

    def get_all_directories(self) -> list:
        directory_nodes = []

        for child in self.children:
            if child.data.data_type == DataType.DIRECTORY:
                directory_nodes.append(child)

        return directory_nodes

    def get_parent(self) -> Node:
        """ Returns the parent if it`s a child otherwise it will return self. """
        return self.parent if self.parent is not None else self

    def get_size_sum(self, size=0):
        size_sum = size

        for child in self.children:
            size_sum += child.get_size_sum(child.data.size)

        return size_sum

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


