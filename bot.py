import os
import time
import math
import json
import string
import random
import traceback
import asyncio
import datetime
import aiofiles
from random import choice
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid
from telethon import TelegramClient, events
from configs import Config
from database import Database

## --- Sub Configs --- ##
# ... (Your existing sub-configs)

source_channel_id = Config.SOURCE_CHANNEL_ID  # Replace with the actual source channel ID or username
destination_channel_id = Config.DESTINATION_CHANNEL_ID  # Replace with the actual destination channel ID or username

# ... (Your existing sub-configs)

# Initialize Telethon client
telethon_client = TelegramClient('telethon_session_name', Config.API_ID, Config.API_HASH)

# ... (Your existing functions)

async def forward_messages(event):
    chat = await event.get_chat()
    if chat.id == source_channel_id:
        await telethon_client.forward_messages(destination_channel_id, event.message)

# ... (Your existing functions)

# Telethon event handler for new messages
@telethon_client.on(events.NewMessage)
async def telethon_event_handler(event):
    await forward_messages(event)

# ... (Your existing functions)

# Telethon client context manager
async def telethon_main():
    async with telethon_client:
        telethon_client.run_until_disconnected()

# ... (Your existing functions)

# Pyrogram client
Bot = Client(Config.BOT_USERNAME, bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH)

# ... (Your existing functions)

# Pyrogram message handler for private messages
@Bot.on_message(filters.private & filters.document | filters.video | filters.audio & ~filters.edited)
async def main(bot, message):
    # ... (Your existing code)
    forwarded_msg = await message.forward(Config.DB_CHANNEL)
    # ... (Your existing code)

# ... (Your existing functions)

# Run the Telethon client in an asyncio event loop
async def run_telethon():
    await telethon_main()

# Run the Pyrogram client
Bot.run()
