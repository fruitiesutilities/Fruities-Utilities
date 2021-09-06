import discord
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
from keep_alive import keep_alive


client = commands.Bot(command_prefix = '>')
status = cycle(['simon says', 'Among us', 'Minecraft', 'no', 'nothing', 'with the mods in the closet'])


@client.event
async def on_ready():
  change_status.start()
  print('Bot is ready')

@tasks.loop(seconds=60)
async def change_status():
  await client.change_presence(status=discord.Status.dnd, activity=discord.Game(next(status)))

@client.command()
@commands.has_permissions(manage_messages=True)
async def eat(ctx, user: discord.User):
  await ctx.send(f'{message.author.send} just ate some random dude. i cant quite remember their name so ill just call them jeff')

@client.command()
async def support(ctx):
  await ctx.send('hey there, i noticed you need support! I will now ping mods for you <@&871708353401847858>')

@client.command()
async def info(ctx):
  await ctx.send('Food world is all about trying to bring users together so that you can make friends and also enjoy your time on discord!')



@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
  await ctx.channel.purge(limit=amount)


@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send('Hey there, why dont you use a command that actually exists!')


@clear.error
async def clear_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(' Next time, tell me how much you want to delete')

@client.command()
async def ping(ctx):
  await ctx.send(f':ping_pong: Pong! My latency is {round(client.latency * 1000)}')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'Kicked {member.mention}')
  return

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'i have banned {user.mention}')
  return

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'Unbanned {user.mention}')
      return

keep_alive()
client.run('Your Token Here')
