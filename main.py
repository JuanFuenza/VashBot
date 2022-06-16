#outdated because ffmpeg not working v: - V
import discord
from discord.ext import commands
import os
from osu import data, check_user, get_user_id, get_osu_name
from tinydb import TinyDB, Query
from datetime import datetime
import youtube_dl

#client = discord.Client()
discord_token = os.environ['TOKEN']
webhook = os.environ['webhook']
client = commands.Bot(command_prefix='|')

osu_user = Query()
db = TinyDB('db.json')


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.command()
async def play(ctx, url: str):
  song_there = os.path.isfile('song.mp3')
  try:
    if song_there:
      os.remove('song.mp3')
  except PermissionError:
    await ctx.send('Espera a que el audio termine o usa el comando "stop".')
    return

  voice_channel = discord.utils.get(ctx.guild.voice_channels, name='Juegos')
  await voice_channel.connect()
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)


  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
  }
  
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  for file in os.listdir('./'):
    if file.endswith('.mp3'):
      os.rename(file, 'song.mp3')
  voice.play(discord.FFmpegPCMAudio('song.mp3'))


@client.command()
async def leave(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_connected():
    await voice.disconnect()
  else:
    await ctx.send('El bot no está conectado al canal de voz.')


@client.command()
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
  else:
    await ctx.send('No hay audio sonando.')


@client.command()
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_paused():
    voice.resume()
  else:
    await ctx.send('El audio no está pausado.')


@client.command()
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()

client.run(discord_token)