import discord
import responses


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
            print(e)

def run_discord_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

#client = commands.Bot(command_prefix='!', intents = intents)

#intents.message_content = True

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private = True)
        else:
            await send_message(message, user_message, is_private=False)

# referances of old stuff, might want it later 

#@client.event
#async def on_message(message):
#    channel = client.get_channel(<channel id>)
#    if message.author == client.user:
#       return

#    if message.content.startswith('tag') and message.channel.id == "<channel id>":
#        await channel.send('*Click* Caught in 4K...')

#@client.command()
#async def tag(ctx):
#    channel = client.get_channel(<channel id>)
#    #if message.content.startswith('!tag') and message.channel.id == "<channel id>":
#    await channel.send(f'*Click* Caught in 4k...')

    # add new token client.run('')
