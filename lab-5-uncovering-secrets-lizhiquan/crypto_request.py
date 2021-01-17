"""
Responsible for housing the Request and other supporting classes
required to capture application configuration settings via command line
arguments.

Classes
--------
- CryptoMode
- IOMode
- CommandLineParser
- Request
"""

import argparse
from enum import Enum


class CryptoMode(Enum):
    """
    Defines the various modes that this crptography program can be
    executed in. Each mode specifies the action that should take place.
    """
    ENCRYPTION = 0
    DECRYPTION = 1


class IOMode(Enum):
    """
    Defines the various modes that specify what the input or output
    format of the program should be.
    """
    CONSOLE = 0
    BINARY_FILE = 1
    TEXT_FILE = 2


class Request:
    """
    The request object represents a request to either encrypt or decrypt
    certain data. The request object comes with certain accompanying
    configuration options as well as a field that holds the result.

    Attributes
    -----------
    - encryption_state: Object of type CryptoMode
    - data_input: String. The data that needs to be encrypted or
    decrypted. This is None if the data is coming in from a file.
    - input_file: String. The file that contains the string to be encrypted or
    decrypted. This is None if the data is not coming from a file and is
    provided directly.
    - input_mode: An IOMode object. Specifies the format of the input.
    - output_mode: An IOMode object. Specifies the format of the output.
    - output_file: String. The name of the output file. Set to None if the
                   output mode is text.
    - key: String. The Key value to use for encryption or decryption.
    - result: String. Placeholder value to hold the result of the
    encryption or decryption. This does not usually come in with the
    request.

    """

    def __init__(self):
        """
        Initialises a request object with all attributes set to None.
        """
        self.encryption_mode = None
        self.data_input = None
        self.input_file = None
        self.output_mode = None
        self.input_mode = None
        self.output_file = None
        self.key = None
        self.result = None

    def __str__(self):
        return f"Request:\n " \
               f"---------\n" \
               f"Crypto Mode: {self.encryption_mode}\n" \
               f"Input Data: {self.data_input}\n" \
               f"Input file: {self.input_file}\n" \
               f"Input Mode: {self.input_mode}\n" \
               f"Output Mode: {self.output_mode}\n" \
               f"Output File: {self.output_file}\n" \
               f"Key: {self.key}\n" \
               f"Result: {self.result}"


class CommandLineParser:
    """
    Utility class that parses command line arguments with the help of
    the built in argsparse module.
    """

    @staticmethod
    def setup_commandline_request() -> Request:
        """
        Defines the command line argument parser and then proceeds to
        parse the command line arguments into a request object. Quits
        the program if unexpected data is provided.
        :return: Request object.
        """
        parser = argparse.ArgumentParser()

        # --------- Crypto Mode ---------
        mode = parser.add_mutually_exclusive_group()
        mode.add_argument("--en", action="store_true",
                          help="Select this to perform encryption.")
        mode.add_argument("--de", action="store_true",
                          help="Select this to perform decryption.")

        # --------- Encryption/Decryption Key ---------
        parser.add_argument("key", help="The key to use when encrypting or "
                                        "decrypting. This needs to be a "
                                        "string of length 8, 16 or 24")

        # --------- Input data ---------
        input_args = parser.add_mutually_exclusive_group()
        input_args.add_argument("--iconsole", help="Select this if the input "
                                                "data is a string. Enter the "
                                                "string data.")
        input_args.add_argument("--ibfile", help="Select this if the input "
                                                 "data is a binary file. "
                                                 "Enter the name of the file.")
        input_args.add_argument("--itfile", help="Select this if the input "
                                                 "data is a text file. Enter "
                                                 "the name of the file.")

        # --------- Output data ---------
        output_args = parser.add_mutually_exclusive_group()
        output_args.add_argument("--oconsole", action="store_true",
                                 help="Select this if the output of the "
                                      "program is a string printed to the "
                                      "console.")
        output_args.add_argument("--obfile",
                                 help="Select this if the output of the "
                                      "program is a binary file. Enter the "
                                      "name of the file.")

        try:
            args = parser.parse_args()
            print(f"DEBUG args: {args.__dict__}")
            request = Request()
            request.key = args.key

            # -- Crypto Mode --
            if args.en:
                request.encryption_mode = CryptoMode.ENCRYPTION
            else:
                request.encryption_mode = CryptoMode.DECRYPTION

            # -- Input --
            if args.iconsole:
                request.data_input = args.iconsole
                request.input_mode = IOMode.CONSOLE
            elif args.ibfile:
                request.input_file = args.ibfile
                request.input_mode = IOMode.BINARY_FILE
            else:
                request.input_file = args.itfile
                request.input_mode = IOMode.TEXT_FILE

            # -- Output --
            if args.oconsole:
                request.output_mode = IOMode.CONSOLE
            else:
                request.output_file = args.obfile
                request.output_mode = IOMode.BINARY_FILE

            return request
        except Exception as e:
            print(f"Error! Could not read arguments.\n{e}")
            quit()
