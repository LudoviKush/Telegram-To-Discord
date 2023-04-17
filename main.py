from telethon import TelegramClient, events
import telethon
import aiohttp
import nextcord
import textwrap
import os
import requests
import json
import random
from discord import SyncWebhook

WEBHOOK_1 = os.environ.get("WEBHOOK_1")
WEBHOOK_2 = os.environ.get("WEBHOOK_2")
appid = os.environ.get("APPID")
apihash = os.environ.get("APIHASH")
apiname = os.environ.get("APINAME")
dlloc = os.environ.get("DLLOC")
input_channels_entities = os.environ.get("INPUT_CHANNELS")
blacklist = os.environ.get("BLACKLIST")

comb = [
  "** Series of messages you want to filter"
]

if blacklist == 'True':
  blacklist = True
if input_channels_entities is not None:
  input_channels_entities = list(map(int, input_channels_entities.split(',')))


async def imgur(mediafile):  # Uploads media to imgur
  url = "https://api.imgur.com/3/upload"

  payload = {'album': 'ALBUMID', 'type': 'file', 'disable_audio': '0'}
  files = [('video', open(mediafile, 'rb'))]
  headers = {'Authorization': str(random.randint(1, 10000000000))}
  response = requests.request("POST",
                              url,
                              headers=headers,
                              data=payload,
                              files=files)
  return (json.loads(response.text))


def start():
  client = TelegramClient(apiname, appid, apihash)
  client.start()
  print('Started: Apiname, appid, apihash', apiname, appid, apihash)
  print(f'Input channels: {input_channels_entities}')
  print(f'Blacklist: {blacklist}')
  print('Connected to the Discord API.')

  @client.on(
    events.NewMessage(chats=input_channels_entities,
                      blacklist_chats=blacklist))
  async def handler(event):
    if (type(event.chat) == telethon.tl.types.User):
      return  #Ignore Messages from Users or Bots
    msg = event.message.message
    if event.message.media is not None:  # If message has media
      dur = event.message.file.duration  # Get duration
      if dur is None:  # If duration is none
        dur = 1  # Set duration to 1
      # If duration is greater than 60 seconds or file size is greater than 200MB Imgur Limit
      if dur > 60 or event.message.file.size > 209715201:
        print('Media too long or too big!')
        chat_id = event.message.chat_id
        chat_id = abs(chat_id)
        print(chat_id, msg)
        result = redirectMessage(chat_id, msg)
        print(result, 'result')
        url = result[0]
        msg = result[1]
        #msg += f"\n\nLink to Video: https://t.me/c/{event.chat.id}/{event.message.id} " + add_msg
        await send_to_webhook(msg, '', event, url)
        return
      else:  # Duration less than 60s send media
        path = await event.message.download_media(dlloc)
        if event.message.file.size > 8388608:  # If file size is greater than 8MB use Imgur
          await picimgur(path, msg, event.chat.title, event)
        else:
          await pic(path, msg, event.chat.title, event)
          #print(path, 'path')
        os.remove(path)
    else:  # No media text message
      chat_id = event.message.chat_id
      chat_id = abs(chat_id)
      print(chat_id, msg)
      result = redirectMessage(chat_id, msg)
      url = result[0]
      msg = result[1]
      print('final message -> ', msg)
      if msg is not None:
        msg = str(msg)
        print(msg, event, url, 'msg,event,url')
        await send_to_webhook(msg, '', event, url)

  client.run_until_disconnected()


async def picimgur(filem, message, username,
                   event):  # Send media to webhook with imgur link
  async with aiohttp.ClientSession() as session:
    try:
      chat_id = event.message.chat_id
      chat_id = abs(chat_id)
      username = fixNames(username)
      result = redirectMessage(chat_id, message)
      url = result[0]
      webhook = nextcord.Webhook.from_url(url, session=session)
      print('Sending w media Imgur')
      try:
        image = await imgur(filem)  # Upload to imgur
        image = image['data']['link']
        print(f'Imgur: {image}')
        await webhook.send(content=image,
                           username=username)  # Send imgur link to discord
      except Exception as ee:
        print(f'Error {ee.args}')
      for line in textwrap.wrap(
          message, 2000, replace_whitespace=False):  # Send message to discord
        await webhook.send(content=line, username=username)
    except Exception as e:
      print(f'Error {e.args}')


async def pic(filem, message, username, event):  # Send media to webhook
  async with aiohttp.ClientSession() as session:
    try:
      chat_id = event.message.chat_id
      chat_id = abs(chat_id)
      username = fixNames(username)
      result = redirectMessage(chat_id, message)
      url = result[0]
      message = result[1]

      print('Sending w media')
      if chat_id != 6942069420:
        #if message is not None:
        webhook = nextcord.Webhook.from_url(url, session=session)
      try:  # Try sending to discord
        f = nextcord.File(filem)
        print(f, "F")
        await webhook.send(file=f, username=username)
      except:  # If it fails upload to imgur
        print('Uploading to imgur')
        try:
          image = await imgur(filem)  # Upload to imgur
          print(image, "filem")
          image = image['data']['link']
          print(f'Imgur: {image}')
          await webhook.send(content=image,
                             username=username)  # Send imgur link to discord
        except Exception as ee:
          print(f'Error {ee.args}')
      for line in textwrap.wrap(
          message, 2000, replace_whitespace=False):  # Send message to discord
        await webhook.send(content=line, username=username)
    except Exception as e:
      print(f'Error {e.args}')


async def send_to_webhook(message, username, event,
                          url):  # Send message to webhook
  async with aiohttp.ClientSession() as session:
    print('Sending w/o media')
    chat_id = event.message.chat_id
    chat_id = abs(chat_id)
    username = fixNames(username)
    result = redirectMessage(chat_id, message)
    url = result[0]
    message = result[1]
    webhook = SyncWebhook.from_url(url)
    for line in textwrap.wrap(
        message, 2000, replace_whitespace=False):  # Send message to discord
      await webhook.send(message
                         )  #webhook.send(content=line, username=username)


def filterCombi(comb, message):
  # Filtering only the needed messages
  for i in comb:
    if i in message:
      print('found combination on', i)
      return message


def redirectMessage(chat_id, message):
  # Send to the webhook based on the chat_id 
  print('coming from:', chat_id)
  if chat_id == 6942069421:
    url = WEBHOOK_2
    print('sending to bolt')
  elif chat_id == 6942069420:
    url = WEBHOOK_1
    #message = filterCombi(comb, message) # !! - Remove the comment here if you want to filter the messages
  else:
    print('else putting in rafting')
    url = WEBHOOK_1

  return url, message


def fixNames(username):
  # Rename the username
  if username == "Group 1": username = "Group 1 Renamed"
  return username


if __name__ == "__main__":
  start()
