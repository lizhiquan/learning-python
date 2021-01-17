"""
This module contains the classes for the commandline parser and request.
Classes:
- QueryMode
- Request
- CommandLineParser
"""
from enum import Enum
import argparse
import re


class QueryMode(Enum):
    """
    The mode that the application will be opened in. This indicates the
    information that the user would like to query.
    """
    POKEMON = 'pokemon'
    ABILITY = 'ability'
    MOVE = 'move'
    ITEM = 'item'
    STAT = 'stat'


class Request:
    """
    The request object represents a request to query Pokedex data. The
    request object comes with certain accompanying configuration options.
    """

    def __init__(self, query_mode: str, inputfile: str, inputdata: str,
                 expanded: bool, output: str):
        """
        Initializes a Request.
        :param query_mode: a str
        :param inputfile: a str
        :param inputdata: a str
        :param expanded: a bool
        :param output: a str
        """
        if inputfile and not re.match(r'.+\.txt', inputfile):
            raise ValueError("Invalid inputfile. The file name must be a .txt"
                             " file.")
        if output and not re.match(r'.+\.txt', output):
            raise ValueError("Invalid output. The file name must be a .txt"
                             " file.")
        self.query_mode = QueryMode(query_mode)
        self.inputfile = inputfile
        self.inputdata = inputdata
        self.expanded = expanded
        self.output = output

    def __str__(self) -> str:
        return f'---Request---\n' \
               f'query_mode: {self.query_mode}\n' \
               f'inputfile: {self.inputfile}\n' \
               f'inputdata: {self.inputdata}\n' \
               f'expanded: {self.expanded}\n' \
               f'output: {self.output}'


class CommandLineParser:
    """
    Utility class that parses command line arguments with the help of
    the built in argsparse module.
    """
    SUPPORTED_MODES = [QueryMode.POKEMON, QueryMode.ABILITY,
                       QueryMode.MOVE, QueryMode.ITEM]
    """
    A list of accepted QueryModes received from the commandline.
    """

    @classmethod
    def setup_commandline_request(cls) -> Request:
        """
        Defines the command line argument parser and then proceeds to
        parse the command line arguments into a request object. Quits
        the program if unexpected data is provided.
        :return: Request object.
        """
        parser = argparse.ArgumentParser()

        # Query mode
        query_modes = [mode.value for mode in cls.SUPPORTED_MODES]
        parser.add_argument("query_mode", choices=query_modes,
                            help="The mode that the application will be opened"
                                 " in")

        # Input
        input_args = parser.add_mutually_exclusive_group(required=True)
        input_args.add_argument("--inputfile", metavar='"filename.txt"',
                                help="Select this if the input data is a "
                                     "text file. The file name must end with a"
                                     " .txt extension. Enter the name of the "
                                     "file.")
        input_args.add_argument("--inputdata", metavar='"name or id"',
                                help="Select this if the input data is just a "
                                     "name or id. The id must be a digit and "
                                     "the name a string. Enter the name or id."
                                )

        # Expanded
        parser.add_argument("--expanded", action="store_true",
                            help="When this flag is provided, certain "
                                 "attributes are expanded, that is the pokedex"
                                 " will do sub-queries to get more information"
                                 " about a particular attribute.")

        # Output
        parser.add_argument("--output", metavar='"filename.txt"',
                            help="If provided, a filename (with a .txt "
                                 "extension) must also be provided. and the "
                                 "query result should be printed to the "
                                 "specified text file.  If this flag is not "
                                 "provided, then print the result to the "
                                 "console.")

        try:
            args = parser.parse_args()
            # print(f"DEBUG args: {args.__dict__}")
            request = Request(**vars(args))
            return request
        except Exception as e:
            print(f"Error! Failed to execute the request. \n{e}")
            quit()
