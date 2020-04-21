# Module Imports
import sys
import json

import requests

from formatting import Formatting

from discord.ext import commands

# Basic Error Classes
class MissingArgument(Exception):
    pass

# Error if no file is provided via argv
if len(sys.argv) == 1:
    
    raise MissingArgument("No file was specified to run.")

# Fetch the code that we need to parse
code = open(sys.argv[1:][0], "r").read()
code = code.split("<htdb>")[1].split("</htdb>")[0]

# Return an error if they are missing a required argument
if not "<token>" in code:
    
    raise MissingArgument("No token was found in the file.")

elif not "<bot prefix=\"" in code:

    raise MissingArgument("No bot instance with a prefix was found in the file.")

# Get data from the code
command_prefix = code.split("<bot prefix=\"")[1].split("\"")[0]

case_sensitive = code.split(f"<bot prefix=\"{command_prefix}\" case_sensitive=")[1].split(">")[0]

bot_token = code.split("<token>")[1].split("</token>")[0]

on_ready_message = ""

if "<ready>" in code:
    
    on_ready_message = code.split("<ready>")[1].split("</ready>")[0]

if case_sensitive:
    
    case_sensitive = False
    
else:
    
    case_sensitive = True

# Basic Bot Instance
bot = commands.Bot(
    command_prefix = command_prefix,
    case_insensitive = case_sensitive
)

# Events
@bot.event
async def on_ready():
    
    """Represents the bot's start message"""
    
    # Hit us up with some formatting for some text options
    start_msg = Formatting.format(on_ready_message, bot)
    
    print(start_msg)

# Command Handler
@bot.event
async def on_message(message):
    
    """Initates and processes all incoming messages and commands"""
    
    # Get an instance of every defined command
    commands = code.split("<commands>")[1].split("</commands>")[0].split("<command name=\"")
    
    # Loop through all the commands
    for command in commands:
        
        # Get lowercase version
        cmd_msg = message.content.lower()
        
        # Remove the arguments from it
        if " " in cmd_msg:
            
            cmd_msg = cmd_msg.split(" ")[0]
            
        # Ignore it if it isn't a command
        if not command_prefix in cmd_msg:
            
            return
        
        # Remove the command prefix from the command
        cmd_msg = cmd_msg.split(command_prefix)[1]
        
        # Get the commands name
        command_name = command.split("\"")[0]
        
        # Initiate if they are the same thing
        if cmd_msg == command_name:
            
            # Get the response text
            text = command.split("<response>")[1].split("</response>")[0]
            
            # Do some formatting to give some more options
            formatted_text = Formatting.format(text, bot, message)

            # Send to channel
            return await message.channel.send(formatted_text)
    
# Connect to the Discord API
bot.run(bot_token)