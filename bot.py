#Main Ichthys backbone
import main.features as features
import main.ui_helper as ui_helper

#Discord.py modules
from discord.ext import commands
import Paginator
import discord
import DiscordUtils

#Other modules
import json
import os
import asyncio
import i18n

#Init Features
biblescraper = features.bible_scraper.BibleScraper()
readingsscraper = features.daily_readings.DailyReadings()
prayers = features.prayers.Prayers()

intents = discord.Intents.default()
client = commands.Bot(command_prefix = '/', intents = intents)

#For translation
current_directory = os.getcwd()
i18n.load_path.append(current_directory + '/locale')
i18n.set('filename_format', 'yml')


@client.event
async def on_ready():
    print("Bot is ready")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

#Help command
@client.tree.command(name="ichthyshelp")
async def ichthyshelp(interaction: discord.Interaction, command: str = ""):

    if command == "":
        embed = discord.Embed(
            title="Ichthys Bot",
            description = i18n.t("about"),
            color=discord.Color.blue()
        )
        embed.add_field(
            name="**🤖 " + i18n.t("help") + " **\n",
            value="`/ichthyshelp read` -" + i18n.t("helpshortdesc") + " /read \n `/ichthyshelp pray` - " + i18n.t("helpshortdesc") + " /pray \n `/ichthyshelp dailyreadings` - "+ i18n.t("helpshortdesc") + " /dailyreadings \n `/ichthyshelp setlocale`" + i18n.t("helpshortdesc") + " /setlocale",
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

    elif command == "read":
        embed = discord.Embed(
            title="Ichthys Read Command",
            description = i18n.t("helpreaddesc"),
            color=discord.Color.blue()
        )
        embed.add_field(name="**" + i18n.t("commandStructure") + "**", value="/read <bible-book><verse>", inline=False)
        embed.add_field(name="**" + i18n.t("exampleCommand") + "**", value="/read John 3:16", inline=False)
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
            list_of_prayers += "/pray " + prayer + "\n"

        list_of_prayers += "\n**Latin Prayers**\n"
        #Read list of latin prayers
        with open("prayers-latin.json") as f:
            prayers_latin = json.load(f, strict=False)

        prayers_latin = prayers_latin.keys()
        for prayer in prayers_latin:
            list_of_prayers += "/pray " + prayer + "\n"

        embed.add_field(name="**" + i18n.t("commandStructure") + "**", value="/pray <prayer-title>", inline=False)
        embed.add_field(name="**" + i18n.t("exampleCommand") + "**", value="/pray hail mary", inline=False)
        embed.add_field(name="**" + i18n.t("listOfAvailablePrayers") + "**", value=list_of_prayers, inline=False)

    elif command == "dailyreadings":
        embed = discord.Embed(
            title="Ichthys Daily Readings Command",
            description = i18n.t("helpreadingsdesc"),
            color=discord.Color.blue()
        )
        embed.add_field(name="**" + i18n.t("commandStructure") + "**", value="/dailyreadings", inline=False)
        embed.add_field(name="**" + i18n.t("exampleCommand") + "**", value="/dailyreadings", inline=False)

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
            list_of_locale += "/setlocale " + locale + " - " + available_locale[locale] + "\n"

        embed.add_field(name="**" + i18n.t("commandStructure") + "**", value="/setlocale <translation>", inline=False)
        embed.add_field(name="**" + i18n.t("exampleCommand") + "**", value=list_of_locale, inline=False)

    else:
        embed = discord.Embed(
            title=i18n.t("commandNotFound"),
            description = i18n.t("commandNotFoundDesc"),
            color=discord.Color.blue()
        )

    await interaction.response.send_message(embed = embed)

#Read command
@client.tree.command(name="read")
async def read(interaction: discord.Interaction, book: str, verse: str):
    read_verse = biblescraper.readVerse(book + verse)
    embed = discord.Embed(
    title=i18n.t("bibleVerseTitle"),
    description = read_verse,
    color=discord.Color.blue()
    )
    await interaction.response.send_message(embed = embed)

#Daily Readings command
@client.tree.command(name="dailyreadings")
async def dailyreadings(interaction: discord.Interaction):

    readings = readingsscraper.dailyReadings()
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

    button_helper = ui_helper.prayers_view.PrayersView(embeds)
    await interaction.response.send_message(embed=embeds[0], view=button_helper)

#Pray command
@client.tree.command(name="pray")
async def pray(interaction: discord.Interaction, title: str):
    prayer = prayers.readPrayer("".join(title[:]).lower())
    embed = discord.Embed(
    title=i18n.t("prayerTitle"),
    description = prayer,
    color=discord.Color.blue()
    )
    await interaction.response.send_message(embed = embed)

#Localization command
@client.tree.command(name="setlocale")
@commands.has_permissions(administrator=True)
async def setlocale(interaction: discord.Interaction, locale: str = "en"):

    i18n.set('locale', locale)
    embed = discord.Embed(
    title=i18n.t("settingLocaleLang"),
    description= i18n.t("botLanguageSet") + " " + locale,
    color=discord.Color.blue()
    )

    await interaction.response.send_message(embed = embed)


client.run(os.environ['BOT_TOKEN'])
