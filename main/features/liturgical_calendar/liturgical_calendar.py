import requests
import json
from datetime import datetime
class LiturgicalCalendar:
    def __init__(self):
        self.info = ""
        self.calendar_url = "http://calapi.inadiutorium.cz/api/v0/en/calendars/default/today"

    def showCalendar(self):
        response = requests.get(self.calendar_url)
        content = json.loads(response.content.decode('utf-8'))


        date = content["date"]
        date_reformat = datetime.strptime(date, "%Y-%m-%d")
        season = content["season"]
        season_week = content["season_week"]
        weekday = content["weekday"]
        celebrations = content["celebrations"]

        celebrations_formatted = []

        for celebration in celebrations:
            if(isinstance(celebration, dict)):
                print(type(celebration))
                title = celebration["title"]
                rank = celebration["rank"]
                
                colour_emoji = ["🟣", "🔴", "🟢", "⚪", "🟡"]

                if celebration["colour"] == "violet":
                    colour = colour_emoji[0]
                elif celebration["colour"] == "red":
                    colour = colour_emoji[1]
                elif celebration["colour"] == "green":
                    colour = colour_emoji[2]
                elif celebration["colour"] == "white":
                    colour = colour_emoji[3] + colour_emoji[4]
                celebrations_formatted.append(colour + "  " + title.capitalize() + ", " + rank.capitalize() + "\n")

        print(celebrations_formatted)


        calendar_description = [date_reformat.strftime("%b %d, %Y"), season.capitalize(), weekday.capitalize(), " ".join(celebrations_formatted)]

        return calendar_description
