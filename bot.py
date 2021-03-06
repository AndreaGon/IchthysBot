import discord
from discord.ext import commands
import scraper
import json
import os
import DiscordUtils

import asyncio

ichthys = scraper.Ichthys()

client = commands.Bot(command_prefix = "+")

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def ichthyshelp(ctx, *, command = ""):


    if command == "":
        embed = discord.Embed(
            title="Ichthys Bot",
            description = "Your all-in-one Catholic Discord Bot",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="**🤖 Help Commands**\n",
            value="`+ichthyshelp read` - Show commands available for +read \n `+ichthyshelp pray` - Show commands available for +pray \n `+ichthyshelp dailyreadings` - Show commands available for +dailyreadings",
            inline=False
        )
        embed.add_field(
            name="**🔗 Links**\n",
            value="**Github** - https://github.com/AndreaGon/IchthysBot",
            inline=False
        )
        embed.set_footer(
            text="Made with ❤ by AndreaGon"
        )
        #embed.add_field(name="**+ichthyshelp read**", value="Show the commands available for +read", inline=False)
        #embed.add_field(name="**+ichthyshelp pray**", value="Show the commands available for +pray", inline=False)
        #embed.add_field(name="**+ichthyshelp dailyreadings**", value="Show the commands available for +dailyreadings", inline=False)
    elif command == "read":
        embed = discord.Embed(
            title="Ichthys Read Command",
            description = "Returns a bible verse based on the user's request",
            color=discord.Color.blue()
        )
        embed.add_field(name="**Command Structure**", value="+read <bible-book><verse>", inline=False)
        embed.add_field(name="**Example Command**", value="+read John 3:16", inline=False)
    elif command == "pray":
        embed = discord.Embed(
            title="Ichthys Pray Command",
            description = "Returns common Catholic prayers",
            color=discord.Color.blue()
        )
        list_of_prayers = ""

        #Read list of prayers (non latin)
        with open("prayers.json") as f:
            prayers = json.load(f, strict=False)

        prayers = prayers.keys()
        for prayer in prayers:
            list_of_prayers += "+pray " + prayer + "\n"

        list_of_prayers += "\n**Latin Prayers**\n"
        #Read list of latin prayers
        with open("prayers-latin.json") as f:
            prayers_latin = json.load(f, strict=False)

        prayers_latin = prayers_latin.keys()
        for prayer in prayers_latin:
            list_of_prayers += "+pray " + prayer + "\n"

        embed.add_field(name="**Command Structure**", value="+pray <prayer-title>", inline=False)
        embed.add_field(name="**Example Command**", value="+pray hail mary", inline=False)
        embed.add_field(name="**List of Available Prayers**", value=list_of_prayers, inline=False)

    elif command == "dailyreadings":
        embed = discord.Embed(
            title="Ichthys Daily Readings Command",
            description = "Returns today's bible readings",
            color=discord.Color.blue()
        )
        embed.add_field(name="**Command Structure**", value="+dailyreadings", inline=False)
        embed.add_field(name="**Example Command**", value="+dailyreadings", inline=False)

    else:
        embed = discord.Embed(
            title="Command Not Found",
            description = "Sorry, but the command you entered does not exist",
            color=discord.Color.blue()
        )

    await ctx.send(embed=embed)


@client.command()
async def read(ctx, book: str, verse: str):
    read_verse = ichthys.readVerse(book + verse)
    embed = discord.Embed(
    title="Bible Verse",
    description = read_verse,
    color=discord.Color.blue()
    )
    await ctx.send(embed = embed)

@client.command()
async def pray(ctx, *title):
    prayer = ichthys.readPrayer(" ".join(title[:]).lower())
    embed = discord.Embed(
    title="Prayer",
    description = prayer,
    color=discord.Color.blue()
    )
    await ctx.send(embed = embed)

@client.command()
async def dailyreadings(ctx):
    readings = ichthys.dailyReadings()
    readings_1 = discord.Embed(
    title="Daily Readings",
    description=readings[0] + readings[1],
    color=discord.Color.blue()
    )
    readings_2 = discord.Embed(
    title="Daily Readings",
    description=readings[2],
    color=discord.Color.blue()
    )
    readings_3 = discord.Embed(
    title="Daily Readings",
    description=readings[3],
    color=discord.Color.blue()
    )
    readings_4 = discord.Embed(
    title="Daily Readings",
    description=readings[4],
    color=discord.Color.blue()
    )

    if len(readings) == 6:
        readings_5 = discord.Embed(
        title="Daily Readings",
        description=readings[5],
        color=discord.Color.blue()
        )
        embeds = [readings_1, readings_2, readings_3, readings_4, readings_5]
    else:
        embeds = [readings_1, readings_2, readings_3, readings_4]

    pages = len(embeds)
    current_page = 1

    message = await ctx.send(embed= embeds[current_page-1])

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=86400, check=check)

            if str(reaction.emoji) == "▶️" and current_page != pages:
                current_page += 1
                await message.edit(embed=embeds[current_page-1])
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and current_page > 1:
                current_page -= 1
                await message.edit(embed=embeds[current_page-1])
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            break

client.run(os.environ['BOT_TOKEN'])
