import requests
from bs4 import BeautifulSoup
import json

class Ichthys:
    def __init__(self):
        self.url = "https://www.biblegateway.com/passage/?search="
        self.readings_url = "https://bible.usccb.org/daily-bible-reading"
    def readVerse(self, verse):
        full_request = self.url + verse + "&version=RSVCE"
        response = requests.get(full_request)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        #Get the whole verse elements first, then extract unnecessary elements
        #Sometimes we will also extract necessary elements for formatting later
        verse_content = soup.find('div', class_='passage-text')
        chapter_header = verse_content.find("h3")
        ignore_full_chapter = verse_content.find('a', class_="full-chap-link")
        ignore_sup_tag = verse_content.find_all('sup', class_="footnote")
        ignore_div_footnote = verse_content.find('div', class_="footnotes")
        ignore_other_trans = verse_content.find('div', class_="passage-other-trans")

        if(ignore_div_footnote != None):
            ignore_div_footnote.extract()

        if(ignore_full_chapter != None):
            ignore_full_chapter.extract()

        if(ignore_other_trans != None):
            ignore_other_trans.extract()

        if(ignore_sup_tag != None):
            for tag in range(len(ignore_sup_tag)):
                ignore_sup_tag[tag].extract()

        if(chapter_header != None):
            chapter_header.extract()
            chapter_header = chapter_header.text
        else:
            chapter_header = verse

        formatted_verse = "**" + chapter_header + "**" + "\n" + verse_content.text + "Read from the website: " + "\n" + full_request

        if len(formatted_verse) > 2000:
            error_message = "It looks like you're reading a Bible verse that has more than 2000 characters. Read instead from the website: \n" + full_request
            return error_message
        return formatted_verse

    def readPrayer(self, prayer):
        with open("prayers.json") as f:
            prayers = json.load(f, strict=False)

        return prayers[prayer]

    def dailyReadings(self):
        response = requests.get(self.readings_url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        readings_info = "Taken from: https://bible.usccb.org/daily-bible-reading"
        readings_content = soup.find_all('div', class_='wr-block b-verse bg-white padding-bottom-m')

        for reading in range(len(readings_content)):
            readings_info += readings_content[reading].text

        return readings_info
