import discord
import logging

client = discord.Client()
logger = logging.getLogger('shotbot_client')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='shotbot_client.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

command_list = {
    "$help": "Display help regarding Discord-ShotBot",
    "$why": "Why was an abomination like me created?",
    "$pour": "Pour Tekktrik a glass",
    "$punish": "He won't learn otherwise"
}

@client.event
async def on_ready():
    logger.info("Logging in successfully as {0.user}, ready to go!".format(client))
    # send message that bot is ready
    
@client.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == client.user:
        return
        
    if message.content == "$why":
        logger.info("{0.author} asked why the hell this even exsits".format(message))
        await message.channel.send("Fuck you, that's why <3\n\
                                    Built with love and too much time")
        
    elif message.content == "$pour":
        logger.info("{0.author} attempted to pour {1.user} shot".format(message, client))
        # pour a shot glass
        
    elif message.content == "$punish":
        logger.info("{0.author} attempted to punish {1.user}, what a jerk".format(message, client))
        # pour all glasses
        
    elif message.content.startswith("$"):
        logger.info("{0.author} seemingly tried to use an invalid command".format(message))
        