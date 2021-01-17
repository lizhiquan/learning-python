from abc import ABC, abstractmethod
from crypto_request import Request
from crypto_request import IOMode

import des


class BaseHandler(ABC):
    """
    Base class for all handlers that handle a request. Each handler can
    maintain a reference to another handler thereby enabling the chain
    of responsibility pattern.
    """

    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def handle_request(self, request: Request) -> bool:
        """
        Each handler would have a specific implementation of how it
        processes a request. This base handler will forward the request
        to the next handler if any and return its result. Otherwise
        return True, indicating the request was handled successfully.
        :param request: a Request
        :return: a boolean indicating the status of the handlers processing
        """
        if not self.next_handler:
            return True
        return self.next_handler.handle_request(request)


class ValidateKeyHandler(BaseHandler):
    """
    This handler is responsible for validating the key in the request to
    make sure it is valid for DES encryption or decryption.
    """

    def handle_request(self, request: Request) -> bool:
        """
        Ensures the key has a length of 8, 16, or 24 characters.
        :param request: a Request
        :return: a bool
        """
        key_length = len(request.key)
        if key_length in [8, 16, 24]:
            return super().handle_request(request)
        return False


class ReadFileHandler(BaseHandler):
    """
    This handler is responsible for reading data from a file and saving
    the result in the Request.data_input field.
    """

    def handle_request(self, request: Request) -> bool:
        """
        Reads the file in the right mode based on the attributes of the
        Request object and saves the result in the Request.data_input
        field.
        :param request: a Request
        :return: a bool
        """
        modes = {
            IOMode.TEXT_FILE: 'r',
            IOMode.BINARY_FILE: 'rb',
        }
        with open(request.input_file, mode=modes[request.input_mode]) as file:
            request.data_input = file.read()
            return super().handle_request(request)


class WriteFileHandler(BaseHandler):
    """
    This class is responsible for writing data from the Request.result
    attribute to a file.
    """

    def handle_request(self, request: Request) -> bool:
        """
        Writes the file in the right mode based on the attributes of the
        Request object.
        :param request: a Request
        :return: a bool
        """
        modes = {
            IOMode.TEXT_FILE: 'w',
            IOMode.BINARY_FILE: 'wb',
        }
        with open(request.output_file, mode=modes[request.output_mode]) \
                as file:
            file.write(request.result)
            return super().handle_request(request)


class EncryptionHandler(BaseHandler):
    """
    This handler is responsible for encrypting the data in request using
    the DES algorithm.
    """

    def handle_request(self, request: Request) -> bool:
        """
        Encrypts the data in the Request.data_input field and stores the
        result in Request.result field.
        :param request: a Request
        :return: a bool
        """
        bin_key = request.key.encode('utf-8')
        des_key = des.DesKey(bin_key)
        bin_data_input = request.data_input.encode('utf-8')
        encrypted_data = des_key.encrypt(bin_data_input, padding=True)
        request.result = encrypted_data
        return super().handle_request(request)


class DecryptionHandler(BaseHandler):
    """
    This handler is responsible for decrypting the data in request using
    the DES algorithm.
    """

    def handle_request(self, request: Request) -> bool:
        """
        Decrypts the data in the Request.data_input field and stores the
        result in Request.result field.
        :param request: a Request
        :return: a bool
        """
        bin_key = request.key.encode('utf-8')
        des_key = des.DesKey(bin_key)
        decrypted_data = des_key.decrypt(request.data_input, padding=True)
        request.result = decrypted_data.decode('utf-8')
        return super().handle_request(request)


class OutputHandler(BaseHandler):
    """
    This handler is responsible for printing the result data to the
    console.
    """

    def handle_request(self, request: Request) -> bool:
        """
        Prints the result to the console.
        :param request: a Request
        :return: a bool
        """
        print(request.result)
        return super().handle_request(request)
