"""
This modules houses the driver class that drives the program.
"""
import asyncio
from cli_request import CommandLineParser, Request, QueryMode
from pokedex_request import PokedexRequestManager
from report import Report, ConsoleOutputStrategy, TextFileOutputStrategy


class Pokedex:
    """
    The driver class that accepts a request and executes it.
    """

    def __init__(self, request: Request):
        """
        Initializes a Pokedex with a request.
        :param request: a Request
        """
        self.request = request
        self.request_manager = PokedexRequestManager()
        output_strategy = TextFileOutputStrategy(request.output) \
            if request.output else ConsoleOutputStrategy()
        self.report_exporter = Report(output_strategy)

    def get_request_dataset(self) -> list:
        """
        Returns a list of request names or ids.
        :return: a list
        """
        if self.request.inputdata:
            return [self.request.inputdata]
        if self.request.inputfile:
            with open(self.request.inputfile, mode='r') as file:
                return [line.strip() for line in file.readlines()]
        return []

    async def fetch_expanded_data(self, pokemons: list) -> None:
        """
        Fetches expanded data of pokemons.
        :param pokemons: a list of Pokemon
        :return: None
        """
        coroutines = [
            asyncio.gather(
                self.request_manager.process_requests(
                    QueryMode.STAT, pokemon.stat_names),
                self.request_manager.process_requests(
                    QueryMode.ABILITY, pokemon.abilities),
                self.request_manager.process_requests(
                    QueryMode.MOVE, pokemon.move_names),
            )
            for pokemon in pokemons
        ]
        expanded_results = await asyncio.gather(*coroutines)
        for pokemon, expanded_result in zip(pokemons, expanded_results):
            stats, abilities, moves = expanded_result
            pokemon.stats = stats
            pokemon.abilities = abilities
            pokemon.moves = moves

    async def execute(self) -> None:
        """
        Execute the request.
        :return: None
        """
        data_set = self.get_request_dataset()
        results = await self.request_manager.process_requests(
            self.request.query_mode, data_set)

        if self.request.expanded and \
                self.request.query_mode == QueryMode.POKEMON:
            await self.fetch_expanded_data(results)

        await self.report_exporter.generate_output(results)


if __name__ == '__main__':
    request = CommandLineParser.setup_commandline_request()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    pokedex = Pokedex(request)
    loop.run_until_complete(pokedex.execute())
