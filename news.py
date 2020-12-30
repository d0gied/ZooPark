import asyncio
import threading
import discord
from config import *
import requests
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# vk
vk_session = vk_api.VkApi(token=VK_TOKEN)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        # Если написали заданную фразу
        if event.from_user:  # Если написали в ЛС
            vk.messages.send(  # Отправляем сообщение
                user_id=event.user_id,
                message='Ваш текст'
            )
        elif event.from_chat:  # Если написали в Беседе
            vk.messages.send(  # Отправляем собщение
                chat_id=event.chat_id,
                message='Ваш текст'
            )

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
        print()


# if antifuck.check(text):
#     await message.delete()
#     return

client.run(TOKEN)
