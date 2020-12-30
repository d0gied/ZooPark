import asyncio
import threading

import discord
from config import *

data_to_print = []

client = discord.Client()
messages = []
available_rooms = [i for i in range(1, 100)]
private_rooms = {}


def discord_print(*args, sep=' ', end='\n'):
    data = list(map(str, args))
    data_to_print.append(sep.join(data) + end)


print = discord_print


async def my_task():
    await client.wait_until_ready()
    last_message = None
    while True:
        if data_to_print:
            channel = client.get_channel(793395529279209493)
            await channel.send(data_to_print.pop(0))
        await asyncio.sleep(0.1)


client.loop.create_task(my_task())
client = discord.Client(loop=client.loop)


@client.event
async def on_ready():
    print(f'{client.user} is connected')


@client.event
async def on_raw_reaction_add(payload):
    message_id = str(payload.message_id)
    if message_id == role_message_id:
        member_role = client.guilds[0].get_role(793342598348800002)
        await payload.member.add_roles(member_role)


@client.event
async def on_message(message: discord.message):
    text = str(message.content).strip()
    channel = message.channel
    member = message.author
    if 'bot' in str(message.author).lower():
        return
    if 'create-room' in channel.name:
        if 'create' in text:
            base = client.get_channel(id=793369624715853845)
            name = base.name + str(available_rooms.pop(0))
            voice_channel = await base.clone(name=name)
            private_rooms[member.name] = voice_channel
            overwrite = discord.PermissionOverwrite()
            await voice_channel.set_permissions(member, connect=True, speak=True, view_channel=True)
            try:
                if member.voice.channel.id == 793339014173294603:
                    await member.move_to(voice_channel)
            except Exception as ex:
                print("Не получилось")
                print(ex)
        if 'add' in text:
            data = text.split('<@!')[1:]
            if data:
                cur_channel = private_rooms.get(member.name, None)
                if cur_channel:
                    for user_str in data:
                        user_id = user_str.split('>')[0]
                        user = client.get_user(int(user_id))
                        await cur_channel.set_permissions(user, connect=True, speak=True, view_channel=True)
                        print(f"`{user.name}` added to `{private_rooms[member.name]}`", sep='')
                else:
                    print(f'Attempt by `{member.name}` to add users without channel')
                    channel.send('Сначала создай комнату')


# if antifuck.check(text):
#     await message.delete()
#     return

client.run(TOKEN)
