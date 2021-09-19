import discord
from discord.ext import commands
from discord.ext import tasks
import time
from itertools import cycle
from keep_alive import keep_alive


client = commands.Bot(command_prefix = '>')
status = cycle(['simon says', 'Among us', 'Minecraft', 'no', 'nothing', 'with the mods in the closet'])

@client.event
async def on_ready():
  change_status.start()
  print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(client))

@tasks.loop(seconds=60)
async def change_status():
  await client.change_presence(status=discord.Status.dnd, activity=discord.Game(next(status)))

@client.command()
@commands.has_permissions(manage_messages=True)
async def eat(ctx, member: discord.Member):
  await ctx.send(f'You just ate {member.mention}! {member.mention} you cannot get unate ')

@client.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, amount):
    try:
        await ctx.channel.edit(reason='Bot Slowmode Command', slowmode_delay=int(amount))
        await ctx.send('Slowmode has been changed. Good job everyone. You made the server slow')
    except discord.Errors.Forbidden:
        await ctx.send('I do not have the permission to do this, please try again')

@client.command()
@commands.has_permissions(manage_messages=True)
async def juice(ctx, member: discord.Member):
  await ctx.send(f'you just juiced {member.mention}! {user.mention} you cannot get unjuiced')

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, time: int, d, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

    for channel in guild.channels:
        await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True)

    await member.add_roles(mutedRole)

    embed = discord.Embed(title="TempMuted!", description=f"{member.mention} has been tempmuted.", colour=discord.Colour.light_gray())
    embed.add_field(name="Reason:", value=reason, inline=False)
    embed.add_field(name="Time for the mute:", value=f"{time}{d}", inline=False)
    await ctx.send(embed=embed)

    if d == "s":
        mutetime = time

    if d == "m":
        mutetime = time*60

    if d == "h":
        mutetime = time*60*60

    if d == "d":
        mutetime = time*60*60*24

    with open("TXT_FILE_PATH", "w+") as mutetimef:
        mutetime.write(mutetime)
    
    while True:
        with open("TXT_FILE_PATH", "w+") as mutetimef:
            if int(mutetimef.read()) == 0:
                await member.remove_roles(mutedRole)

                embed = discord.Embed(title="Unmute (temp mute expired) ", description=f"Unmuted -{member.mention} ", colour=discord.Colour.light_gray())
                await ctx.send(embed=embed)
  
                return
            else:
                mutetime -= 1
                mutetimef.seek(0)
                mutetimef.truncate()
                mutetimef.write(mutetime)
        await asyncio.sleep(1)

@client.command()
@commands.has_permissions(manage_messages=True)
async def unjuice(ctx, member: discord.Member):
  await ctx.send(f'you just unjuiced {member.mention}! {user.mention} say thank you to this person')

@client.command()
async def roleinfo(ctx, role: discord.Role):
  await ctx.send(f'This is a really cool role called {role.mention}. Its ID is {role.id} and it seems like it is in the server you ran this command in :smile:')

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmuted from: - {ctx.guild.name}")
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages=True)
async def rejuice(ctx, member: discord.Member):
  await ctx.send(f'you just rejuiced {member.mention}! {user.mention} you cannot get unjuiced')

@client.command()
async def userinfo(ctx, member: discord.Member):
  await ctx.send(f'{member.mention} is a cool person inside of Food world. Their ID is {member.id} and their discriminator tag is {member.discriminator}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def uneat(ctx, member: discord.Member):
  await ctx.send(f'You just unate {member.mention}! {member.mention} say thank you to that person for uneating you!')

@client.command()
async def support(ctx):
  await ctx.send('hey there, i noticed you need support! I will now ping support for you <@&871708353401847858>')

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
  await ctx.send(f':ping_pong: Pong! My latency is {round(client.latency * 1000)}ms')

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
  await ctx.send(f'banned {member.mention}')
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
      await ctx.send(f'Unbanned {member.mention}')
      return

keep_alive()
client.run('your token here')
