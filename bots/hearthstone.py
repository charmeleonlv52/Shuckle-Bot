import aiohttp

from config import config

from shuckle.command import command
from shuckle.data import TempDownload
from shuckle.error import ShuckleError
from shuckle.util import gen_help

CARD_DISPLAY = '''
**{name}**
Set: {cardSet}
Flavor Text: {flavor}
'''

SEARCH_DISPLAY = '''
Here is a list of Hearthstone cards containing **{}**:
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
    headers = {
        'content-type': 'application/json',
        'X-Mashape-Key': config.mashape_key
    }

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self):
        '''
        Show hearth commands:
        ```
        @{bot_name} hearth help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command()
    async def search(self, args):
        '''
        Lists cards that contain a search string (min length: 3):
        ```
        @{bot_name} hearth search <card>
        ```
        '''
        card = ' '.join(args)

        if len(card) < 3:
            raise ShuckleError('Please provide a longer search string.')

        route = SEARCH_CARD.format(card)
        headers = self.headers

        with aiohttp.ClientSession() as session:
            async with session.get(route, headers=headers) as resp:
                if resp.status == 404:
                    raise ShuckleError('No results found.')
                elif resp.status == 200:
                    body = await resp.json()
                    cards = '\n'.join([x['name'] for x in body])
                    await self.client.say(SEARCH_DISPLAY.strip().format(card, cards))
                else:
                    raise ShuckleError('Unable to get card information. Try again later.')

    @command()
    async def card(self, args):
        '''
        Shows information about a specific card:
        ```
        @{bot_name} hearth card <card>
        ```
        '''
        card = ' '.join(args)

        route = SINGLE_CARD.format(card)
        headers = self.headers

        with aiohttp.ClientSession() as session:
            async with session.get(route, headers=headers) as resp:
                # This isn't an actual card. Try searching
                # for it and returning the result.
                if resp.status == 404:
                    await self.search(args)
                elif resp.status == 200:
                    body = await resp.json()
                    body = body[0]
                    name = body['name']
                    image = body['img']

                    async with TempDownload(image) as path:
                        with open(path, 'rb') as f:
                            await self.client.upload(f, content=CARD_DISPLAY.strip().format(**body))
                else:
                    raise ShuckleError('Unable to get card information. Try again later.')

bot = HearthBot
