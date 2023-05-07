import discord
from typing import List

class PrayersView(discord.ui.View):
    def __init__(self, embeds: [str]):
        super().__init__(timeout=150)
        self.embeds = embeds
        self.current_page = 0;

    @discord.ui.button(label = "Previous")
    async def prevButton(self, interaction: discord.Interaction, _: discord.ui.Button):
        if self.current_page >= 0:
            self.current_page -= 1
        else:
            self.current_page = len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current_page])
        #return discord.ui.Button(label = self.prev_title)

    @discord.ui.button(label = "Next")
    async def nextButton(self, interaction: discord.Interaction, _: discord.ui.Button):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
        else:
            self.current_page = 0
        await interaction.response.edit_message(embed=self.embeds[self.current_page])
        #return discord.ui.Button(label = self.next_title)
