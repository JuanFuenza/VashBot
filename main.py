import discord
from discord.ext import commands
import os
import json
from osu import data, check_user, get_user_id, get_osu_name
from tinydb import TinyDB, Query
from datetime import datetime
from pprint import pprint

client = discord.Client()
discord_token = os.environ['TOKEN']
webhook = os.environ['webhook']

osu_user = Query()
db = TinyDB('db.json')

def search(disc_user):
  results = db.search(osu_user.disc_user == disc_user)
  return results

def get_users():
  disc_user = [r['disc_name'].split('#')[0] for r in db]
  return disc_user

def validate_user(validated):
  validated = db.search(osu_user.disc_user == validated)
  if validated:
    return True
  else:
    return False

def get_time():
  today = f'{datetime.now()}'.split('.')[0]
  return today


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if msg.startswith('|rs'):
    disc_user = str(message.author.id)
    try:
      user_search = db.search(osu_user.disc_user == disc_user)[0]['disc_user']
      if user_search == disc_user:
        user_id = db.search(osu_user.disc_user == disc_user)[0]['user_id']
        osu_name = db.search(osu_user.disc_user == disc_user)[0]['osu_name']
  
        try:
            ec = data(user_id)
            
            embed = discord.Embed(
            description = f'▸ **{ec[8]}** ▸ **{ec[7]}** ▸ {ec[10]} \n▸ {ec[9]} ▸ x{ec[3]}/{ec[4]} ▸ [{ec[11]}/{ec[12]}/{ec[13]}]\n▸**map completation:** ',
            colour = discord.Colour.blue()
          )
      
            embed.set_footer(icon_url='https://images-ext-1.discordapp.net/external/3OqZdghI9tf65Q2rzB0_gGR9bek8r8eVjzkJc77yFOw/https/i.imgur.com/Req9wGs.png',text=get_time())
            embed.set_thumbnail(url=ec[18])
            embed.set_author(name =ec[16]+' +'+ec[6]+f'[{ec[17]}★]', url=ec[0], icon_url='https://cdn.discordapp.com/avatars/892070695041912843/85f9f137449d1a3004c4ea68c207294b.webp?size=32')
            await message.channel.send(f'Recent osu! Standard Play for {ec[1]}:')
            await message.channel.send(embed=embed)
        except:
          await message.channel.send(f'{osu_name} has no recent plays in Bancho for osu! Standard')
    except:
      await message.channel.send('Usuario no registrado o invalido.')

  if msg.startswith('|register'):
    register = msg.split('|register ',1)[1]
    
    if not validate_user(str(message.author.id)):
      if check_user(register):
        user_id = get_user_id(register)
        disc_user = str(message.author.id)
        disc_name = str(message.author)
        osu_name = get_osu_name(register)
        db.insert({'user_id': user_id,'osu_name':osu_name,'disc_user':disc_user,'disc_name':disc_name})
        await message.channel.send('Usuario Registrado.')
      else:
        await message.channel.send('Este usuario no existe.')
    else:
      await message.channel.send('Tu ID de discord ya está asociada a una cuenta.')

  if msg.startswith('|users'):
    await message.channel.send(get_users())

  if msg.startswith('|help'):
    eh = discord.Embed(description = '|rs = Muestra tu play más reciente\n|register "osu_user" = Registra tu usuario de osu!\n|users = Muestra los usuarios registrados\n|delete = Borra tu usuario registrado.',
        colour = discord.Colour.blue(),
                       inline=True
    )
    await message.channel.send(embed=eh)

  if msg.startswith('|delete'):
    disc_user = str(message.author.id)
    try:
      result = db.search(osu_user.disc_user == disc_user)[0]['disc_user']
      
      if result == disc_user:
        db.remove(osu_user.disc_user == disc_user)
        
        await message.channel.send('Usuario removido exitosamente.')
      else:
        await message.channel.send('Usuario no encontrado o ya removido.')
    except:
      await message.channel.send('Usuario no encontrado o ya removido.')


client.run(discord_token)