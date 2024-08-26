import asyncio
from datetime import datetime, timedelta
from os import path, listdir
from shutil import rmtree
from random import choice
import logging
from json import JSONDecodeError
from instagrapi import Client
from RedDownloader import RedDownloader

client = Client()
client.login('username', 'password')
print('Successfully logged in')

logging.basicConfig(level=logging.WARNING)

downloading = 'disabled' # False or 'disabled'

def fetch_inbox_sync():
    return client.direct_threads()

def process_message_sync(message):
    global downloading
    try:
        if message.user_id != client.user_id:
            current_time = datetime.now()
            time_range_start = current_time - timedelta(seconds=10)
            time_range_end = current_time + timedelta(seconds=10)

            if time_range_start <= message.timestamp <= time_range_end:
                text = message.text
                print(f'New message detected (within range of ±10 seconds)! ID: {message.id}')
                print(f'Text: {text}')
                image_path = get_random_image()
                print(f'Image: {image_path}')

                if text and text.lower() == 'cat':
                    client.direct_send('Downloading cat...', [message.user_id])
                    if downloading is False or downloading == 'disabled':
                        try:
                            if path.exists(image_path):
                                client.direct_send_file(image_path, [message.user_id])
                                client.direct_send(f'Cat downloaded! 😸', [message.user_id])
                            else:
                                client.direct_send("Failed to download cat. 😿 Try again now or later", [message.user_id])
                        except Exception as e:
                            print(f"An unexpected error occurred while sending a message: {e}")
                    else:
                        client.direct_send('Sorry, I am downloading another cat right now. 😿', [message.user_id])
    except KeyError as e:
        print(f"KeyError: {e} - Skipping this message.")

def download_cat_sync():
    global downloading

    if downloading != 'disabled':
        if downloading is False:
            if path.exists('downloaded'):
                rmtree('downloaded')
            
            downloading = True

            while True:
                files = RedDownloader.DownloadImagesBySubreddit('cat', 5, 'new')
                downloading = False
                return files
                
    return []

def get_random_image(download_dir='downloaded'):
    items = [f for f in listdir(download_dir) if path.join(download_dir, f)]

    if not items:
        return None

    selected_item = choice(items)
    selected_path = path.join(download_dir, selected_item)

    if path.isfile(selected_path):
        return selected_path
    elif path.isdir(selected_path):
        inner_items = [f for f in listdir(selected_path) if path.isfile(path.join(selected_path, f))]

        if inner_items:
            return path.join(selected_path, choice(inner_items))

    return None

async def main():
    if downloading != 'disabled':
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, download_cat_sync)

    while True:
        loop = asyncio.get_event_loop()
        inbox = await loop.run_in_executor(None, fetch_inbox_sync)

        for thread in inbox:
            for message in thread.messages:
                await loop.run_in_executor(None, process_message_sync, message)

        await asyncio.sleep(2.5)

try:
    asyncio.run(main())
except JSONDecodeError as e:
    print(f"JSON decode error: {e}")
