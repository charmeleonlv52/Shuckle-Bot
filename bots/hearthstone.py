curl --get --include 'https://omgvamp-hearthstone-v1.p.mashape.com/cards/leeroy%20jenkins' \
  -H 'X-Mashape-Key: uAN2N2GQYYmshZq6F4beo3U0KWVLp1b3ydQjsnHcjwFV6v0LZN' \
  -H 'Accept: application/json'

import aiohttp
import json

from config import config

from shuckle.command import command

CARD_DISPLAY = '''
**{name}**
Set: {cardSet}
Type: {type}
Class: {faction}
Rarity: {rarity}
Stats: {attack}/{health}
Image: {img}
'''

SEARCH_DISPLAY = '''
Here is a list of cards that contain {}:
{}
'''

SINGLE_CARD = 'https://omgvamp-hearthstone-v1.p.mashape.com/cards/{}'
SEARCH_CARD = 'https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/{}'

class HearthBot(object):
    '''
    **Hearth Bot**
    Provides commands to show information about Hearthstone.
    '''
    __group__ = 'hearth'
    headers = {'content-type': 'application/json'}
    payload = {'X-Mashape-Key': config.mashape_key}

    def __init__(self, client):
        self.client = client

    @command()
    async def search(self, card):
        card = ' '.join(card)

        if len(card) < 3:
            raise ShuckleError('Please provide a longer search string.')

        args = [
            SEARCH_CARD.format(card),
            data=json.dumps(self.payload),
            headers=self.headers
        ]

        with aiohttp.ClientSession() as session:
            async with session.get(*args) as resp:
                if resp.status == 404:
                    raise ShuckleError('No results found.')
                elif resp.status == 200:
                    body = await resp.json()
                    cards = '\n'.join()[x['name'] for x in body])
                    await self.say(SEARCH_DISPLAY.strip().format(card, cards))
                else:
                    raise ShuckleError('Unable to get card information. Try again later.')

    @command()
    async def card(self, card):
        card = ' '.join(card)

        args = [
            SINGLE_CARD.format(card),
            data=json.dumps(self.payload),
            headers=self.headers
        ]

        with aiohttp.ClientSession() as session:
            async with session.get(*args) as resp:
                # This isn't an actual card. Try searching
                # for it and returning the result.
                if resp.status == 404:
                    await self.search(card)
                elif resp.status == 200:
                    body = await resp.json()
                    await self.say(CARD_DISPLAY.strip().format(*body))
                else:
                    raise ShuckleError('Unable to get card information. Try again later.')
