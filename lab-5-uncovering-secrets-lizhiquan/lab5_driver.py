"""
The entry point into the program. Module is responsible for housing the driver
class and parsing command line arguments.

Classes
--------
- CryptoDriver
"""

import crypto_handlers
from crypto_request import Request
from crypto_request import CommandLineParser
from crypto_request import CryptoMode
from crypto_request import IOMode


class CryptoDriver:
    """
    Drives the cryptography program and is responsible for handler chain setup
    and subsequent processing of an encryption/decryption request.
    """

    def __init__(self, request: Request):
        """
        Initializes a CryptoDriver with a request object that has been parsed
        via the command line.
        :param request: Request object.
        """
        self.request = request
        self.handler_chain_head = self.setup_handlers()

    def setup_handlers(self) -> crypto_handlers.BaseHandler:
        """
        Sets up a chain of handlers and returns the header of the chain.
        :return: a BaseHandler
        """
        validate_key_handler = crypto_handlers.ValidateKeyHandler()
        encryption_handler = crypto_handlers.EncryptionHandler()
        output_handler = crypto_handlers.OutputHandler()
        read_file_handler = crypto_handlers.ReadFileHandler()
        write_file_handler = crypto_handlers.WriteFileHandler()
        decryption_handler = crypto_handlers.DecryptionHandler()

        if self.request.encryption_mode == CryptoMode.ENCRYPTION:
            if self.request.input_mode == IOMode.CONSOLE:
                # Encrypt console text input and output the result to the
                # console
                if self.request.output_mode == IOMode.CONSOLE:
                    validate_key_handler.next_handler = encryption_handler
                    encryption_handler.next_handler = output_handler

                # Encrypt the console text input and output the result to a
                # binary file
                elif self.request.output_mode == IOMode.BINARY_FILE:
                    validate_key_handler.next_handler = encryption_handler
                    encryption_handler.next_handler = write_file_handler

            elif self.request.input_mode == IOMode.TEXT_FILE:
                # Encrypt input from a text file and output the result to the
                # console
                if self.request.output_mode == IOMode.CONSOLE:
                    validate_key_handler.next_handler = read_file_handler
                    read_file_handler.next_handler = encryption_handler
                    encryption_handler.next_handler = output_handler

                # Encrypt input from a text file and output the result to a
                # binary file
                elif self.request.output_mode == IOMode.BINARY_FILE:
                    validate_key_handler.next_handler = read_file_handler
                    read_file_handler.next_handler = encryption_handler
                    encryption_handler.next_handler = write_file_handler

        elif self.request.encryption_mode == CryptoMode.DECRYPTION:
            # Decrypt a binary file and output the result to the console
            if self.request.input_mode == IOMode.BINARY_FILE and \
                    self.request.output_mode == IOMode.CONSOLE:
                validate_key_handler.next_handler = read_file_handler
                read_file_handler.next_handler = decryption_handler
                decryption_handler.next_handler = output_handler

        return validate_key_handler

    def execute_request(self) -> None:
        """
        Executes the request and prints the result to console.
        :return: None
        """
        status = self.handler_chain_head.handle_request(request)
        if status:
            print('The task is finished successfully!')
        else:
            print('Something went wrong! Failed to execute this task!')


if __name__ == '__main__':
    request = CommandLineParser.setup_commandline_request()
    # print(f"DEBUG REQUEST: \n{request}")

    driver = CryptoDriver(request)
    driver.execute_request()
