"""
This module contains three classes and is meant to contain code that
facilitates HTTP web requests as well as code to output the results.
"""
import asyncio
import aiohttp
import aiofiles
import enum
import starwars_entities


class OutputMode(enum.Enum):
    """
    Enumerates the different supported output formats. This class should
    be used to dynamically generate menus and to dynamically determine
    how a request should be outputted.
    """
    TEXTFILE = "Text File"
    CONSOLE = "Console"


class RequestMode(enum.Enum):
    """
    Enumerates the different supported request formats. This class should
    be used to dynamically generate menus and to dynamically determine
    the endpoint of a request.
    """
    STARSHIPS = "starships"
    PLANETS = "planets"


class StarWarsRequestManager:
    """
    Manages HTTP GET requests to the Star Wars API
    (https://swapi.dev/api). Comprised of the following interface:

    Class Variables:
        + ENDPOINT: An unformatted endpoint that should be formatted
                    before attempting a request
        + entity_mapper: A dictionary that maps the type of request to
                        the entity that the response represents.
                        Currently supports Starships and Planets.

    Attributes:
        + request_mode: An enum specifying the type of request and
                        response to expect.
        + output_mode: An enum specifying the type of output. The
                       manager currently supports console output
                       and text files
        + get_request (async): Asynchronous method to conduct a single
                               http get request
        + output (async): Asynchronous method to output the responses
                          of a single web request
        + process_requests (async): Asynchronous method to process
                                    multiple HTTP get requests.
    """

    """
    Unformatted endpoint. Format this with request mode ({0}) and 
    request id ({1})
    """
    ENDPOINT = "https://swapi.dev/api/{0}/{1}"

    """
    A dictionary that maps the type of request to the entity that the 
    response represents. Currently supports Starships and Planets.
    """
    entity_mapper = {
        RequestMode.STARSHIPS: starwars_entities.Starship,
        RequestMode.PLANETS: starwars_entities.Planet,
    }

    def __init__(self, request_mode: RequestMode, output_mode: OutputMode):
        """
        An instance of the StarWars Request Manager supports a single
        request type and output format.
        :param request_mode: An object of type RequestMode (Enum)
        :param output_mode: An object of type OutputMode (Enum)
        """
        self.request_mode = request_mode
        self.output_mode = output_mode

    async def get_request(self, session: aiohttp.ClientSession,
                          url: str) -> dict:
        """
        Utilizes the aiohttp module to conduct a single HTTP web request
        to the specified target url
        :param session: An active aiohttp.ClientSession
        :param url: a string, must be a formatted version of the
                    endpoint.
        :return: a dict, JSON representation of the response
        """
        response = await session.request(method="GET", url=url)
        json_response = await response.json()
        return json_response

    async def output(self, response_obj, filename: str = None):
        """
        Outputs the result of the web request (instantiated object, not
        JSON dictionary) to the correct channel based on the output mode
        of this instance. If the output mode is text file, this method
        utilizes the aiofiles package to write asynchronously.
        :param response_obj: an instantiated object made up of the
                             attributes specified in the response of a
                             web request. Currently supports Starship
                             and Planet
        :param filename: The name of the file to write to. Defaults to
                         None. Must be provided if the output mode is
                         TEXTFILE
        :return: None
        """
        if self.output_mode == OutputMode.CONSOLE:
            print(response_obj)
        elif self.output_mode == OutputMode.TEXTFILE:
            async with aiofiles.open(filename, mode='w') as file:
                await file.write(str(response_obj))

    async def process_requests(self, data_set: list):
        """
        Instantiates an active aiohttp Client session and processes
        multiple HTTP GET requests.
        :param data_set: a sequence type that contains the different id
                         or names to query.
        :return: None
        """
        async with aiohttp.ClientSession() as session:
            list_urls = [self.ENDPOINT.format(self.request_mode.value,
                                              request_id)
                         for request_id in data_set]
            coroutines = [self.get_request(session, url) for url in list_urls]
            responses = await asyncio.gather(*coroutines)
            items = []
            for response in responses:
                try:
                    item = self.entity_mapper[self.request_mode](**response)
                except Exception as e:
                    print(f'Error: {e}')
                    print(f'Response: {response}')
                else:
                    items.append(item)

            coroutines = [self.output(item, f'response_{item.name}.txt'
                          if self.output_mode == OutputMode.TEXTFILE else None)
                          for item in items]
            await asyncio.gather(*coroutines)
