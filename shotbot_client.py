import discord
import logging
import os
import time
from dotenv import load_dotenv

client = discord.Client()
logger = logging.getLogger('shotbot_client')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='shotbot_client.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
logger.debug("Used load_dotenv() to load environment")

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('GUILD_NAME')
SPECIFIED_CHANNEL_NAME = os.getenv('SPECIFIED_CHANNEL_NAME')

logger.debug("DISCORD_TOKEN: {0}".format(DISCORD_TOKEN))
logger.debug("GUILD_NAME: {0}".format(GUILD_NAME))
logger.debug("SPECIFIED_CHANNEL_NAME: {0}".format(SPECIFIED_CHANNEL_NAME))

command_prefix = "$"

command_list = {
    "help":     "help",
    "about":    "why",
    "pour":     "pour",
    "fill":     "punish"
}

def getCommandFor(input_string):
    return command_prefix+command_list[input_string]

command_help = {
    getCommandFor("help"): "Display help regarding Discord-ShotBot (That's this)",
    getCommandFor("about"): "Why was an abomination like me created?",
    getCommandFor("pour"): "Pour {0.user} a glass".format(client),
    getCommandFor("fill"): "{0.user} won't learn otherwise".format(client)
}

class CommandTimer:
    
    def __init__(self, single_lockout=10, fill_lockout=60):
    
        self._single_lockout_sec = single_lockout*60
        self._fill_lockout_sec = fill_lockout*60
        self._single_unlock_time = time.time()
        self._fill_unlock_time = time.time()
        self._in_progress_lock = False
        self._user_lock = False
        
    def isSingleTimerReady(self):
        return True if (time.time() >= self._single_unlock_time) else False
        
    def isFillTimerReady(self):
        return True if (time.time() >= self._fill_unlock_time) else False
        
    def resetTimers(self):
        self._single_unlock_time = time.time() + self._single_lockout_sec
        self._fill_unlock_time = time.time() + self._fill_lockout_sec
        
    def getTimerTimeRemaining(self):
        single_time_remain = self._single_unlock_time - time.time()
        fill_time_remain = self._fill_unlock_time - time.time()
        return single_time_remain, fill_time_remain
        
    def setInProgress(self):
        self._in_progress_lock = True
        
    def markProgressComplete(self):
        self._in_progress_lock = False
        
    def isInProgress(self):
        return self._in_progress_lock
        
    def setUserLockOn(self):
        self._user_lock = True
        
    def setUserLockOff(self):
        self._user_lock = False
        
    def isUserLockSet(self):
        return self._user_lock
        
command_timer = CommandTimer()

@client.event
async def on_ready():
    logger.info("Logging in successfully as {0.user}, ready to go!".format(client))
    # send message that bot is ready
    
@client.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == client.user:
        return
        
    # Only work with messages from the specified server
    if message.guild.name != GUILD_NAME:
        logger.debug("Logged message from {0.author} from server \"{0.guild.name}\" ({0.guild.id}): {0.content}".format(message))
        return
    
    # Ignore message from non-specified channels
    if message.channel.name != SPECIFIED_CHANNEL_NAME:
        return
        
    is_pour_command = (message.content == getCommandFor("pour"))
    is_fill_command = (message.content == getCommandFor("fill"))
        
    if message.content == getCommandFor("about"):
        logger.info("{0.author} asked why the hell this even exsits".format(message))
        await message.channel.send(
            "Fuck you, that's why <3\n\
            Built with love and too much time"
        )
    
    elif (is_pour_command or is_fill_command):
        logger.debug("Pouring command registered")
        
        if command_timer.isInProgress():
            single_timer_remaining, fill_timer_remaining = command_timer.getTimerTimeRemaining()
            single_remaining_str = str(int(single_timer_remaining))+":"+str(round((single_timer_remaining-int(single_timer_remaining))*60))
            fill_remaining_str = str(int(fill_timer_remaining))+":"+str(round((fill_timer_remaining-int(fill_timer_remaining))*60))
            logger.info("Damn, {0.author} really wanted to make {1.user} drink, but the timer isn't up!".format(message, client))
            logger.info("Time remaining for single pour: {}".format(single_remaining_str))
            logger.info("Time remaining for full pour: {}".format(fill_remaining_str))
            choose_time_remaining = single_remaining_str if is_pour_command else fill_remaining_str
            await message.channel.send("Woah, woah, woah - slow down there, {0.author}!  {1.user} still has about {2} left before you can do that!".format(message, client, choose_time_remaining))
            return
            
        if command_timer.isUserLockSet():
            logger.info("User lockout is set, will not pour shot(s)")
            await message.channel.send("Sorry, {0.author}!  Looks like {1.user} isn't ready for another one yet!".format(message, client))
            return
        
        if is_pour_command:
            logger.info("{0.author} attempted to pour {1.user} shot".format(message, client))
            # pour a shot glass
            
        else:
            logger.info("{0.author} attempted to punish {1.user}, what a jerk".format(message, client))
            # pour all glasses
        
    elif message.content == getCommandFor("help"):
        logger.info("{0.author} asked for help".format(message))
        help_message = ""
        for command, help_text in command_help.items():
            help_message += "".join(command, ": ", help_text, "\n")
        help_message += "".join("\n", "Created by Tekktrik using Python")
        await message.channel.send(help_message)
        
    elif message.content.startswith(command_prefix):
        logger.info("{0.author} seemingly tried to use an invalid command".format(message))
        await message.channel.send("Beep boop, does not compute.  Try using $help command.")
    
    return
        
client.run(DISCORD_TOKEN)