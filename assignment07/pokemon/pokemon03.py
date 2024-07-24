import aiofiles
import asyncio
import json

pokemonapi_directory = './assignment07/pokemon/pokemonapi'
pokemonmove_directory = './assignment07/pokemon/pokemonmove'

async def main():
    # Read the contents of the json file.
    async with aiofiles.open(f'{pokemonapi_directory}/articuno.json', mode='r') as f:
        contents = await f.read()

    # Load it into a dictionary and create a list of moves.
    pokemon = json.loads(contents)
    name = pokemon['name']
    moves = [move['move']['name'] for move in pokemon['moves']]
    
    async with aiofiles.open(f'{pokemonapi_directory}/{name}_moves.txt', mode='w') as f:
        await f.write('\n'.join(moves))
        
asyncio.run(main())
