import discord
from discord.ext import commands
import scraper
import json

ichthys = scraper.Ichthys()

client = commands.Bot(command_prefix = "+")

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def ichthyshelp(ctx, *, command = ""):


    if command == "":
        embed = discord.Embed(
            title="Ichthys Bot Help Commands",
            description = "This contains a list of Ichthys bot commands",
            color=discord.Color.blue()
        )
        embed.add_field(name="**+ichthyshelp read**", value="Show the commands available for +read", inline=False)
        embed.add_field(name="**+ichthyshelp pray**", value="Show the commands available for +pray", inline=False)
        embed.add_field(name="**+ichthyshelp dailyreadings**", value="Show the commands available for +dailyreadings", inline=False)
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

        with open("prayers.json") as f:
            prayers = json.load(f, strict=False)

        prayers = prayers.keys()
        for prayer in prayers:
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
    embed = discord.Embed(
    title="Daily Readings",
    description= readings,
    color=discord.Color.blue())

    await ctx.send(embed=embed)
client.run('ODc0NDc4NTU0NTA1Njg3MTAw.YRHjng.3yTJa7sbgelgJVvrYuAcAmU6GMY')
