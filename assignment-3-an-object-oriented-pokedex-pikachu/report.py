"""
This module is responsible for printing to the console and/or
writing to a file.

Classes:
- Report
- TextFileOutputStrategy
- ConsoleOutputStrategy
"""
import aiofiles
import datetime


class Report:
    """Handles Output for the Program"""

    def __init__(self, output_strategy):
        """
        Initializes a Report.
        :param output_strategy: an OutPutStrategy based on --output flag
        """
        self.output_strategy = output_strategy

    async def generate_output(self, data: list) -> None:
        """
        Generates output from given strategy.
        :param data: a list, of data entries
        :return: None
        """
        await self.output_strategy.generate_output(data)


class TextFileOutputStrategy:
    """Strategy for outputting to text files"""

    def __init__(self, output_file: str):
        """
        Initializes a TextFileOutputStrategy.
        :param output_file: a str
        """
        self.output_file = output_file

    async def generate_output(self, data: list) -> None:
        """
        Writes data to the given file.
        :param data: a list, of data entries
        :return: None
        """
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        async with aiofiles.open(self.output_file, mode="w") as file:
            await file.write(f"Timestamp: {timestamp}\n")
            await file.write(f"Number of Entries: {len(data)}\n\n")
            for item in data:
                await file.write(str(item))
                await file.write('------------------------------------\n\n')


class ConsoleOutputStrategy:
    """Strategy for outputting to to the console"""

    async def generate_output(self, data: list) -> None:
        """
        Prints output to the console.
        :param data: a list of data entries
        :return: None
        """
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        print(f'\n{timestamp}')
        print(f'Number of Entries: {len(data)}\n')
        for item in data:
            print(item)
            print(40*'-')
