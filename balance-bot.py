"""
Simple Python-based Discord bot that reads reactions to a message and assigns fair teams, based on methods supplied by users

Author: Daniel Li
"""

import itertools
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from balancer import Balancer

# Uses python-dotenv to store the Discord API key and secret
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Commands are prefaced by ">"
bot = commands.Bot(command_prefix=">")

# Initializes skill array
skills = {}

# Keep track of users who have responded because you don't want duplicates
users_responded = []

# Test command, please ignore!
@bot.command(name="go")
async def greeting(ctx):

    quotes = ["Hello everybody", "I am pretty good today"]

    response = random.choice(quotes)
    await ctx.send(response)

# Error handler that for now, handles invalid arguments to commands. I will add more later
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send("You typed in an invalid parameter. Please try again.")
    else:
        await ctx.send("You did something wrong, please try again")

# Registers a player into a matchmaking pool. If they already registered, will update the user's skill.
@bot.command(name="setskill")
async def setskill(ctx, skill: int):
    if ctx.message.author.mention in users_responded:
        await ctx.send(
            f"{ctx.message.author.mention}, you have updated your skill from {skills[ctx.message.author.mention]} to {skill}"
        )
        skills[ctx.message.author.mention] = skill
    else:
        skills[ctx.message.author.mention] = skill
        await ctx.send(
            f"{ctx.message.author.mention}, you have registered your skill as level {skill}"
        )
        users_responded.append(ctx.message.author.mention)


@bot.command(name="balance")
async def balance(ctx, method: str):
    balancer = Balancer(skills, method)
    try:
        team1, team1_sum, team2, team2_sum = balancer.balance_teams()
        await ctx.send(
            "**Team 1:**\n"
            + balancer.to_string(team1)
            + "\nSum: "
            + str(team1_sum)
            + "\n\n"
        )
        await ctx.send(
            "**Team 2:**\n" + balancer.to_string(team2) + "\nSum: " + str(team2_sum)
        )
    # Returns a more specific error (odd players, no players, etc.)
    except ValueError:
        error = balancer.balance_teams()
        await ctx.send(error)


@bot.command(name="listplayers")
async def listplayers(ctx):
    if len(skills) == 0:
        await ctx.send("No players have registered themselves to the team matchmaking")
    else:
        await ctx.send("Current Participants:")
        for key, value in skills.items():
            await ctx.send(f"{key} | Skill: {value}")

# Resets the matchmaking pool
@bot.command(name="flushplayers")
async def flushplayers(ctx):
    skills.clear()
    await ctx.send("Match participant list has been flushed")


bot.run(TOKEN)
