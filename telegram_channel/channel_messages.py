'''
This script connects to Telegram API and is able to fetch all existing messages from a user defined channel.

For authentication purposes, user must first obtain an unique api_id, api_hash from https://my.telegram.org/auth?to=apps

Read more documentation from https://core.telegram.org/api.
'''
import configparser
import json
import asyncio
from datetime import date, datetime
import re
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

# Function to parse only required attributes
def filter_message_data(message):
    return {
        "_": message["_"],
        "id": message["id"],
        "peer_id": message["peer_id"],
        "date": message["date"],
        "message": message.get("message"),
        "views": message.get("views"),
        "forwards": message.get("forwards"),
        "replies": message.get("replies"),
        "edit_date": message.get("edit_date"),
        "post_author": message.get("post_author"),
        "grouped_id": message.get("grouped_id"),
        "reactions": message.get("reactions"),
    }

# DateTimeEncoder to handle custom JSON serialization
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)

# Function to get the channel name and use it as file name
def get_channel(name):
    # Extract the channel name from URLs like https://t.me/TheStraitsTimes
    match = re.search(r't\.me/([A-Za-z0-9_]+)', name)
    return match.group(1) if match else name

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    user_input_channel = input('enter entity(telegram URL or entity id):')

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    # tracker to count the number of fetch
    offset_id = 0

    # set limit to 100 messages for each fetch
    limit = 100

    # tracker to count the number of messages fetched
    total_messages = 0
    total_count_limit = 0
    all_messages = []

    while True:
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            filtered_message = filter_message_data(message.to_dict())
            all_messages.append(filtered_message)
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    # # get user_input_channel for file name
    channel_name = get_channel(user_input_channel)

    # Generate dynamic file name using user_input_channel and timestamp
    file_name = f'{channel_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

    # Save beautified JSON to file (for readability)
    with open(file_name, 'w', encoding='utf-8') as outfile:
        json.dump(all_messages, outfile, cls=DateTimeEncoder, indent=4, ensure_ascii=False)

    print(f"Messages saved to {file_name}")

with client:
    client.loop.run_until_complete(main(phone))
