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
    logger.info("Logging in successfully as {0.user}, ready to go!")
    # send message that bot is ready
    
@client.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == client.user:
        return
        
    if message.content.startswith("$why")
        await message.channel.send("Fuck you, that's why")
        
    