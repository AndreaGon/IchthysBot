import requests
from bs4 import BeautifulSoup
import json
import datetime
import pytz

class Ichthys:
    def __init__(self):
        self.timezone = pytz.timezone('Asia/Singapore')
        self.current_time = datetime.datetime.now(self.timezone)
        self.current_month = "{:02d}".format(self.current_time.month)
        self.current_day = "{:02d}".format(self.current_time.day)
        self.current_year = str(self.current_time.year % 100)
        self.url = "https://www.biblegateway.com/passage/?search="
        self.readings_url = "https://bible.usccb.org/bible/readings/" + self.current_month + self.current_day + self.current_year + ".cfm"
    def readVerse(self, verse):
        full_request = self.url + verse + "&version=RSVCE"
        response = requests.get(full_request)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        #Get the whole verse elements first, then extract unnecessary elements
        #Sometimes we will also extract necessary elements for formatting later
        verse_content = soup.find('div', class_='version-RSVCE result-text-style-normal text-html')

        verses_format = []
        for verse in verse_content.find_all():
            if verse.name == 'h3':
                verses_format.append("\n"+ "**" + verse.text + "**" + "\n\n")
            elif verse.name == 'p':
                ignore_sup_tag = verse.find('sup', class_="footnote")
                if(ignore_sup_tag == None):
                    verses_format.append(verse.text + "\n")

        verses_format.append("\n\nRead from the website: \n" + full_request)
        if len(verses_format) > 2000:
            error_message = "It looks like you're reading a Bible verse that has more than 2000 characters. Read instead from the website: \n" + full_request
            return error_message


        return "".join(verses_format)



    def readPrayer(self, prayer):
        with open("prayers.json") as f:
            prayers = json.load(f, strict=False)

        return prayers[prayer]

    def dailyReadings(self):
        response = requests.get(self.readings_url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        readings_info = "Taken from: " + self.readings_url
        readings_content = soup.find_all('div', class_='wr-block b-verse bg-white padding-bottom-m')

        for reading in range(len(readings_content)):
            readings_info += readings_content[reading].text

        return readings_info
