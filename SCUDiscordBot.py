  
import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions
from discord.ext.commands import MemberNotFound
import random
import asyncio
import os
import youtube_dl

#role ID
student = 831240165606817902
freshman = 831232089554157608
sophomore = 831232126883201095
junior = 831232167085604884
senior = 831232194559213629

global onGoingTimer
onGoingTimer = False

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="BIGGIE ", intents=intents)

@client.event
async def on_ready():
    global main_message
    main_message = await client.get_channel(831240097533788180).fetch_message(831286812714336287) #welcome-channel and my message
    await main_message.add_reaction("🤡")
    await main_message.add_reaction("😩")
    await main_message.add_reaction("😳")
    await main_message.add_reaction("🥵")
    activity = discord.Game(name="Use \"BIGGIE help\" for help!", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
   

@client.command(help="Start the pomodoro with inputed values")
async def study(ctx, Study=25, shortBreak=5, bigBreak=15):
    global onGoingTimer

    if onGoingTimer:
        await ctx.send("Timer already in progress!")
        return

    channel = ctx.author.voice
    if channel == None:
        await ctx.send("Please join a VC first.")
        return

    channel = ctx.author.voice.channel

    vc = await channel.connect()
    
    onGoingTimer = True
    try:
        client.loop.create_task(timer(ctx,Study, shortBreak, bigBreak, 0, 1, vc))
        await ctx.send("Timer started!")
        vc.play(discord.FFmpegPCMAudio(source="ring2.mp3"))
    except:
        await ctx.send("Something went wrong!")

    client.loop.create_task(check(ctx, vc))
    
    

@client.command(pass_context=True, help="ends the pomodoro")
async def studystop(ctx):
    vc = ctx.message.guild.voice_client

    if vc == None:
        return
    await ctx.voice_client.disconnect()
    global onGoingTimer
    onGoingTimer = False
    await ctx.send("Nap time!")
    
@client.command(name='play_song', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")
    
    
@client.command(pass_context=True)
async def ping(ctx):
    ''' @pong! '''
    await ctx.send('{0} Pong!'.format(ctx.author.mention))

@client.event
async def on_member_join(member): 
    rank = discord.utils.get(member.guild.roles, id=student)
    await member.add_roles(rank)

@client.command(pass_context=True,help="changes your role to the desired one")
async def changerole(ctx, roles):

    if roles == None:
        await ctx.send('Please enter a role.')
        return

    roles = roles.lower()
    if roles == "freshman": 
        await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, id=freshman))
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=sophomore))
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=junior))
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=senior))
        await ctx.send('{0} Your role has been changed to {1}'.format(ctx.author.mention, roles))
    elif roles == "sophomore":
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=freshman)) 
        await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, id=sophomore))
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=junior))
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=senior))
        await ctx.send('{0} Your role has been changed to {1}'.format(ctx.author.mention, roles))
    elif roles == "junior": 
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=freshman))
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=sophomore))
        await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, id=junior))
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=senior))
        await ctx.send('{0} Your role has been changed to {1}'.format(ctx.author.mention, roles))
    elif roles == "senior": 
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=freshman))
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=sophomore))
        await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, id=junior))
        await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, id=senior))
        await ctx.send('{0} Your role has been changed to {1}'.format(ctx.author.mention, roles))
    else:
        await ctx.send('Role not found :(')




@client.command(pass_context=True, help="Kicks the user you mentioned")
@commands.has_permissions(kick_members=True)
async def fuck(ctx, Member: discord.Member):
    try:
        await Member.kick()
        await ctx.send("Goodbye {0}".format(Member.mention))
    except:
        print("Kick failed")

@fuck.error
async def fuck_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to do that!")
    elif isinstance(error, MemberNotFound):
        await ctx.send("I wasn't able to find that user :(")
    else:
        await ctx.send("I wasn't able to kick that user :(")



# @client.command(pass_context=True)
# async def lofi(ctx):

# @client.command(pass_context=True)
# async def bangers(ctx):

# @client.command(pass_context=True)
# async def selfie(ctx):
    
    # random = random.randint(0,9)


    # await channel.send(file=discord.File('my_image.png'))


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 831286812714336287:
        user = payload.member
        if payload.emoji.name == "🤡":
            await user.add_roles(discord.utils.get(user.guild.roles, id=831232089554157608))
        elif payload.emoji.name == "😩":
            await user.add_roles(discord.utils.get(user.guild.roles, id=831232126883201095))
        elif payload.emoji.name == "😳":
            await user.add_roles(discord.utils.get(user.guild.roles, id=831232167085604884)) 
        elif payload.emoji.name == "🥵":
            await user.add_roles(discord.utils.get(user.guild.roles, id=831232194559213629))
        
        await user.remove_roles(discord.utils.get(user.guild.roles, id=831240165606817902))

        #https://stackoverflow.com/questions/63418818/python-discord-bot-python-clear-reaction-clears-all-reactions-instead-of-a-s
        message = main_message
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        inter_total = ["🤡", "😩","😳","🥵"]

        if user.id != client.user.id and payload.emoji.name not in inter_total:
            await reaction.remove(payload.member)


async def timer(ctx, studyCnt, sbreak, bbreak, cnt , bCnt, vc):
    shortBreak = False
    longBreak = False
    
    cnt = float(cnt)
    sbreak = float(sbreak)
    bbreak = float(bbreak)
    studyCnt = float(studyCnt)

    while onGoingTimer:
        if shortBreak:
            if cnt < (sbreak* 60):
                await asyncio.sleep(1)
                cnt = cnt + 1
            else:
                await ctx.send("Your {0} minute(s) break is over, Study time!".format(sbreak))
                shortBreak = False
                cnt = 0
                vc.play(discord.FFmpegPCMAudio(source="ring2.mp3"))
        elif longBreak:
            if cnt < (bbreak * 60):
                await asyncio.sleep(1)
                cnt = cnt + 1
            else:
                await ctx.send("Your {0} minute(s) break is over, Study time!".format(bbreak))
                longBreak = False
                cnt = 0
                vc.play(discord.FFmpegPCMAudio(source="ring2.mp3"))
        else:
            if cnt < (studyCnt* 60):
                await asyncio.sleep(1)
                cnt = cnt + 1
            elif bCnt % 3:
                await ctx.send("{0} minute(s) has passed, Short break!".format(studyCnt))
                shortBreak = True
                cnt = 0
                bCnt = bCnt + 1
                vc.play(discord.FFmpegPCMAudio(source="ring2.mp3"))
            else:
                await ctx.send("{0} minute(s) has passed, Long break!".format(studyCnt))
                longBreak = True
                cnt = 0
                bCnt = bCnt + 1
                vc.play(discord.FFmpegPCMAudio(source="ring2.mp3"))



async def check(ctx,vc):
    global onGoingTimer
    while onGoingTimer:
        if vc == None:
            return
        member_count = len(vc.channel.members)
        if member_count == 1:
            await ctx.send("I've been abandoned :(")
            await ctx.voice_client.disconnect()
            onGoingTimer = False
        await asyncio.sleep(30)


client.run(os.environ['token'])