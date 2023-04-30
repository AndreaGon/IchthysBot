import discord

class Buttons():
    def __init__(self):
        self.next_title = "Next"
        self.prev_title = "Previous"

    def nextButton(self):
        return discord.ui.Button(label = self.next_title)

    def prevButton(self):
        return discord.ui.Button(label = self.prev_title)
