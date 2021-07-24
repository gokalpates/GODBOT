import os
import discord
from server import keep_running

intents = discord.Intents.all()

client = discord.Client(intents=intents)

token = os.environ['token']
master_id_string = os.environ["master_id"]
master_id_int = int(master_id_string)

@client.event
async def on_ready():
  print("Log: Logged in as {0.user}"
  .format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Pornhub"))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.author.id == master_id_int:
    if not message.content.startswith(">>"):
      return
    elif message.content == ">> pin":
      await pin_last(message)  
    elif ">> delete msg" in message.content:
      await delete(message)
    elif ">> write" in message.content:
      await write(message)
    elif message.content == ">> info":
      await info(message)
    elif ">> say" in message.content:
      await say(message)
    elif ">> create txt" in message.content:
      await create_text_ch(message)
    elif ">> create voice" in message.content:
      await create_voice_ch(message)
    elif message.content == ">> list members":
      await list_members(message)
    elif ">> create category" in message.content:
      await create_category(message)
    elif ">> kick named" in message.content:
      await kick_named(message)
    elif ">> kick id" in message.content:
      await kick_id(message)
    elif ">> ban named" in message.content:
      await ban_named(message)
    elif ">> ban id" in message.content:
      await ban_id(message)
    elif ">> purge" in message.content:
      await purge(message)
    elif ">> delete txt" in message.content:
      await delete_txt(message)
    elif ">> delete voice" in message.content:
      await delete_voice(message)
    elif ">> delete category" in message.content:
      await delete_category(message)
    elif ">> wipe voice" in message.content:
      await wipe_voice(message)
    elif ">> wipe all voice" in message.content:
      await wipe_all_voice(message)

  else:
    return

async def pin_last(message):
  counter = 0
  async for m in message.channel.history(limit=2):
    if counter == 1:
      await m.pin()
    counter += 1

async def delete(message):
  number_string = message.content[message.content.rfind(" "):]
  number = int(number_string)
  async for m in message.channel.history(limit=number):
    await m.delete()

async def write(message):
  number_string = message.content[message.content.rfind(" "):]
  number = int(number_string)

  content_string = message.content[message.content.find("\"") + 1: message.content.rfind("\"")]
  
  for i in range(number):
    await message.channel.send(content_string)

async def info(message):
  info = """hello @everyone, i am an extremely overpowered bot only at Gökalp Ateş's disposal. I only listen to my master's commands, my master honors me by making me stronger in his spare time."""
  await message.channel.send(info)

async def say(message):
  await message.channel.last_message.delete()
  content_string = message.content[message.content.find("\"")+1: message.content.rfind("\"")]

  await message.channel.send(content_string)
  
async def create_text_ch(message):
  text_ch_name = message.content[message.content.find("\"") + 1: message.content.rfind("\"")]

  await message.guild.create_text_channel(text_ch_name)

async def create_voice_ch(message):
   voice_ch_name = message.content[message.content.find("\"") + 1: message.content.rfind("\"")]

   await message.guild.create_voice_channel(voice_ch_name)

async def list_members(message):
  member_list = message.guild.members
  member_message  = ""
  for member in member_list:
    member_message += member.name + ":\t" + str(member.id) + "\n"
  await message.channel.send(member_message)

async def create_category(message):
  category_name = message.content[message.content.find("\"") + 1: message.content.rfind("\"")]

  await message.guild.create_category(category_name)

async def kick_named(message):
  target_name = message.content[message.content.find("\"")+1:message.content.rfind("\"")]
  target = message.guild.get_member_named(target_name)
  await target.kick()

async def kick_id(message):
  target_id_string = message.content[message.content.find("\"") + 1:message.content.rfind("\"")]
  target_id_int = int(target_id_string)
  target = message.guild.get_member(target_id_int)
  await target.kick()

async def ban_named(message):
  target_id_string = message.content[message.content.find("\"") + 1:message.content.rfind("\"")]
  target = message.guild.get_member_named(target_id_string)
  await target.ban()

async def ban_id(message):
  target_id_string =message.content[message.content.find("\"") + 1:message.content.rfind("\"")]
  target_id_int = int(target_id_string)
  target = message.guild.get_member(target_id_int)
  await target.ban()

async def purge(message):
  await message.channel.purge()

async def delete_txt(message):
  txt_ch_name = message.content[message.content.find("\"") + 1:message.content.rfind("\"")]
  for txt_ch in message.guild.text_channels:
    if txt_ch.name == txt_ch_name:
      await txt_ch.delete()
      return

async def delete_voice(message):
  voice_ch_name = message.content[message.content.find("\"") + 1:message.content.rfind("\"")]
  for voice_ch in message.guild.voice_channels:
    if voice_ch.name == voice_ch_name:
      await voice_ch.delete()
      return

async def delete_category(message):
  category_name = message.content[message.content.find("\"") + 1:message.content.rfind("\"")]
  for cat_item in message.guild.categories:
    if cat_item.name == category_name:
      await cat_item.delete()
      return

async def wipe_voice(message):
  voice_ch_name = message.content[message.content.find("\"") + 1:message.content.rfind("\"")]
  for voice_ch in message.guild.voice_channels:
    if voice_ch.name == voice_ch_name:
      for member in voice_ch.members:
        await member.move_to(None)

async def wipe_all_voice(message):
  for voice_ch in message.guild.voice_channels:
    for member in voice_ch.members:
      await member.move_to(None)

keep_running()
client.run(token)
