"""
This module houses graph classes that act as observers.
It contains:
 - Graph
 - LineGraph
 - BarGraph
 - TableGenerator
"""
from abc import ABC, abstractmethod
from typing import List
from pandas import Series
from matplotlib import pyplot as plt
from prettytable import PrettyTable


class Graph(ABC):
    """
    Represents a graph.
    """

    @abstractmethod
    def __call__(self, title: str, data: List[Series], labels: List[str],
                 output_name: str) -> None:
        """
        An abstract method to generates a graph and saves it to a file.
        :param title: a str, the title of the graph
        :param data: a list of Series
        :param labels: a list of str, the titles of columns
        :param output_name: a str, the name of the output file
        :return: None
        """
        pass


class LineGraph(Graph):
    """
    Represents a line graph.
    """

    def __init__(self, line_style: str, has_fill: bool, fill_colour: str):
        """
        Initializes a LineGraph.
        :param line_style: a str
        :param has_fill: a bool
        :param fill_colour: a str
        """
        self.line_style = line_style
        self.has_fill = has_fill
        self.fill_colour = fill_colour

    def __call__(self, title: str, data: List[Series], labels: List[str],
                 output_name: str) -> None:
        """
        Generates a line graph and saves it to a file.
        :param title: a str, the title of the graph
        :param data: a list of Series
        :param labels: a list of str, the titles of columns
        :param output_name: a str, the name of the output file
        :return: None
        """
        plt.clf()
        plt.figure(figsize=(9, 6))
        plt.plot(data[0], data[1], linestyle=self.line_style,
                 color=self.fill_colour)
        if self.has_fill:
            plt.fill_between(data[0], data[1], interpolate=True,
                             color=self.fill_colour)
        plt.title(title)
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])
        plt.savefig(f'{output_name}_line.png')


class BarGraph(Graph):
    """
    Represents a bar graph.
    """

    def __init__(self, is_horizontal: bool, edge_colour: str, bar_colour: str):
        """
        Initializes a LineGraph.
        :param is_horizontal: a bool
        :param edge_colour: a str
        :param bar_colour: a str
        """
        self.is_horizontal = is_horizontal
        self.edge_colour = edge_colour
        self.bar_colour = bar_colour

    def __call__(self, title: str, data: List[Series], labels: List[str],
                 output_name: str) -> None:
        """
        Generates a bar graph and saves it to a file.
        :param title: a str, the title of the graph
        :param data: a list of Series
        :param labels: a list of str, the titles of columns
        :param output_name: a str, the name of the output file
        :return: None
        """
        plt.clf()
        plt.figure(figsize=(9, 6))
        if self.is_horizontal:
            plt.barh(data[0], data[1], color=self.bar_colour,
                     edgecolor=self.edge_colour)
            plt.xlabel(labels[1])
            plt.ylabel(labels[0])
        else:
            plt.bar(data[0], data[1], color=self.bar_colour,
                    edgecolor=self.edge_colour)
            plt.xlabel(labels[0])
            plt.ylabel(labels[1])
        plt.title(title)
        plt.savefig(f'{output_name}_bar.png')


class TableGenerator:
    """
    Represents a table.
    """

    def __init__(self, align: str):
        """
        Initializes a TableGenerator.
        :param align: a str
        """
        self.align = align

    def __call__(self, title: str, data: List[Series], labels: List[str],
                 output_name: str) -> None:
        """
        Generates a table and saves it to a file.
        :param title: a str, the title of the graph
        :param data: a list of Series
        :param labels: a list of str, the titles of columns
        :param output_name: a str, the name of the output file
        :return: None
        """
        table = PrettyTable()
        for i in range(len(labels)):
            table.add_column(labels[i], data[i])
        table_txt = table.get_string()
        with open(f'{output_name}_table.txt', 'w') as file:
            file.write(table_txt)
