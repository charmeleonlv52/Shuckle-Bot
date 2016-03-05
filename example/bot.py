from shuckle.command import command

# An example bot with the following usage:
# 	@<bot name> example hello
# 	>hello <your name>

class Example(object):
	__group__ = 'example'

	def __init__(self, client):
		self.client = client

	@command()
	async def hello(self, frame):
		await self.client.say('hello {}'.format(frame.author.name))

bot = Example
