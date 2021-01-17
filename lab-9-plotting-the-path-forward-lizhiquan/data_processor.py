"""
This module houses the DataProcessor class, which is the core and also
known as the Publisher.
"""
import pandas


class DataProcessor:
    """
    This class is responsible for processing the data and notifying its
    observers whenever the internal state changes.
    """

    def __init__(self):
        """
        Initializes a DataProcessor.
        """
        self.callbacks = []

    def subscribe_callbacks(self, *args) -> None:
        """
        Accepts a variable number of callback objects and adds them to
        the list of callbacks.
        :param args: callable objects
        :return: None
        """
        self.callbacks.extend(args)

    def process_data(self, excel_file: str, output_title: str) -> None:
        """
        Reads the excel file into a data frame using pandas and extracts
        the two columns.
        :param excel_file: a str, path of excel file
        :param output_title: a str, name of output file
        :return: None
        """
        df = pandas.read_excel(excel_file)
        for callback in self.callbacks:
            data = [df[col] for col in df.columns]
            callback(output_title.capitalize(), data, df.columns.tolist(),
                     output_title)
