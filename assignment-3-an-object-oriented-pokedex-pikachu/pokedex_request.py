"""
This module contains the PokedexRequestManager for the program.
"""
import asyncio
import aiohttp
import pokemon
from cli_request import QueryMode


class PokedexRequestManager:
    """
    Manages HTTP GET requests to the Pokedex API.
    """

    ENDPOINT = "https://pokeapi.co/api/v2/{0}/{1}/"
    """
    Unformatted endpoint. Format this with query mode (0) and id or
    name (1).
    """

    entity_mapper = {
        QueryMode.POKEMON: pokemon.Pokemon,
        QueryMode.ABILITY: pokemon.PokemonAbility,
        QueryMode.MOVE: pokemon.PokemonMove,
        QueryMode.ITEM: pokemon.PokemonItem,
        QueryMode.STAT: pokemon.PokemonStat,
    }
    """
    A dictionary that maps the type of query to the entity that the 
    response represents.
    """

    async def get_request(self, session: aiohttp.ClientSession,
                          url: str) -> aiohttp.ClientResponse:
        """
        Utilizes the aiohttp module to conduct a single HTTP web request
        to the specified target url
        :param session: An active aiohttp.ClientSession
        :param url: a string, must be a formatted version of the
                    endpoint.
        :return: an aiohttp.ClientResponse
        """
        response = await session.request(method="GET", url=url)
        return response

    async def process_requests(self, query_mode: QueryMode,
                               data_set: list) -> list:
        """
        Instantiates an active aiohttp Client session and processes
        multiple HTTP GET requests.
        :param query_mode: a QueryMode
        :param data_set: a sequence type that contains the different id
                         or names to query.
        :return: a list of requested items.
        """
        async with aiohttp.ClientSession() as session:
            list_urls = [self.ENDPOINT.format(query_mode.value, request_id)
                         for request_id in data_set]
            coroutines = [self.get_request(session, url) for url in list_urls]
            responses = await asyncio.gather(*coroutines)
            results = []
            for response in responses:
                try:
                    json_response = await response.json()
                    item = self.entity_mapper[query_mode](**json_response)
                except Exception as e:
                    print(f'Error: {e}')
                    # print(f'Response: {response}')
                else:
                    results.append(item)

            return results
