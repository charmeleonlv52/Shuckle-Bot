from shuckle.command import command

class Example(object):
	__group__ = 'example'

	def __init__(self, client):
		self.client = client

	@command
	async def say_hi():
		await self.client.say('hi')

bot = Example