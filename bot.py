import discord
from discord.ext import commands
import scraper
import json
import os
import DiscordUtils

import asyncio

import i18n

ichthys = scraper.Ichthys()

client = commands.Bot(command_prefix = "+")

#For translation
i18n.load_path.append("locale")
i18n.set('filename_format', 'tl.yml')

@client.event
async def on_ready():
    print(i18n.t("help"))
    print("Bot is ready")

@client.command()
async def ichthyshelp(ctx, *, command = ""):

    if command == "":
        embed = discord.Embed(
            title="Ichthys Bot",
            description = i18n.t("help"),
            color=discord.Color.blue()
        )
        embed.add_field(
            name="**🤖 " + i18n.t("help") + " **\n",
            value="`+ichthyshelp read` -" + i18n.t("helpshortdesc") + " +read \n `+ichthyshelp pray` - " + i18n.t("helpshortdesc") + " +pray \n `+ichthyshelp dailyreadings` - "+ i18n.t("helpshortdesc") + " +dailyreadings \n `+ichthyshelp setlocale`" + i18n.t("helpshortdesc") + " +setlocale",
            inline=False
        )
        embed.add_field(
            name="**🔗 " + i18n.t("links") + " **\n",
            value="**Github** - https://github.com/AndreaGon/IchthysBot" + "\n **Love Offerings** - https://www.buymeacoffee.com/andreagon",
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
            description = i18n.t("helpreaddesc"),
            color=discord.Color.blue()
        )
        embed.add_field(name="**" + i18n.t("commandStructure") + "**", value="+read <bible-book><verse>", inline=False)
        embed.add_field(name="**" + i18n.t("exampleCommand") + "**", value="+read John 3:16", inline=False)
    elif command == "pray":
        embed = discord.Embed(
            title="Ichthys Pray Command",
            description = i18n.t("helppraydesc"),
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

        embed.add_field(name="**" + i18n.t("commandStructure") + "**", value="+pray <prayer-title>", inline=False)
        embed.add_field(name="**" + i18n.t("exampleCommand") + "**", value="+pray hail mary", inline=False)
        embed.add_field(name="**" + i18n.t("listOfAvailablePrayers") + "**", value=list_of_prayers, inline=False)

    elif command == "dailyreadings":
        embed = discord.Embed(
            title="Ichthys Daily Readings Command",
            description = i18n.t("helpreadingsdesc"),
            color=discord.Color.blue()
        )
        embed.add_field(name="**" + i18n.t("commandStructure") + "**", value="+dailyreadings", inline=False)
        embed.add_field(name="**" + i18n.t("exampleCommand") + "**", value="+dailyreadings", inline=False)

    elif command == "setlocale":
        embed = discord.Embed(
            title="Ichthys Set Locale Command",
            description = i18n.t("helptranslationsdesc"),
            color=discord.Color.blue()
        )

        list_of_locale = ""


        #Read list of latin prayers
        with open("locale/available_locale.json") as f:
            available_locale = json.load(f, strict=False)

        locale_keys = available_locale.keys()
        for locale in locale_keys:
            list_of_locale += "+setlocale " + locale + " - " + available_locale[locale] + "\n"

        embed.add_field(name="**" + i18n.t("commandStructure") + "**", value="+setlocale <translation>", inline=False)
        embed.add_field(name="**" + i18n.t("exampleCommand") + "**", value=list_of_locale, inline=False)

    else:
        embed = discord.Embed(
            title=i18n.t("commandNotFound"),
            description = i18n.t("commandNotFoundDesc"),
            color=discord.Color.blue()
        )

    await ctx.send(embed=embed)


@client.command()
async def read(ctx, book: str, verse: str):
    read_verse = ichthys.readVerse(book + verse)
    embed = discord.Embed(
    title=i18n.t("bibleVerseTitle"),
    description = read_verse,
    color=discord.Color.blue()
    )
    await ctx.send(embed = embed)

@client.command()
async def pray(ctx, *title):
    prayer = ichthys.readPrayer(" ".join(title[:]).lower())
    embed = discord.Embed(
    title=i18n.t("prayerTitle"),
    description = prayer,
    color=discord.Color.blue()
    )
    await ctx.send(embed = embed)

@client.command()
async def dailyreadings(ctx):
    readings = ichthys.dailyReadings()
    readings_1 = discord.Embed(
    title=i18n.t("dailyReadingsTitle"),
    description=readings[0] + readings[1],
    color=discord.Color.blue()
    )
    readings_2 = discord.Embed(
    title=i18n.t("dailyReadingsTitle"),
    description=readings[2],
    color=discord.Color.blue()
    )
    readings_3 = discord.Embed(
    title=i18n.t("dailyReadingsTitle"),
    description=readings[3],
    color=discord.Color.blue()
    )
    readings_4 = discord.Embed(
    title=i18n.t("dailyReadingsTitle"),
    description=readings[4],
    color=discord.Color.blue()
    )

    if len(readings) == 6:
        readings_5 = discord.Embed(
        title=i18n.t("dailyReadingsTitle"),
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



@client.command()
@commands.has_permissions(administrator=True)
async def setlocale(ctx, locale:str = "en"):

    i18n.set('locale', locale)
    embed = discord.Embed(
    title=i18n.t("settingLocaleLang"),
    description= i18n.t("botLanguageSet") + " " + locale,
    color=discord.Color.blue()
    )

    await ctx.send(embed=embed)

client.run(os.environ['BOT_TOKEN'])
