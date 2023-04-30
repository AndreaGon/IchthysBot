import requests
from bs4 import BeautifulSoup
import json
import pytz
import os

class BibleScraper:
    def __init__(self):
        self.timezone = pytz.timezone('Asia/Singapore')
        self.url = "https://www.biblegateway.com/passage/?search="

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
                 if ignore_sup_tag != None:
                     ignore_sup_tag.extract()
                 verses_format.append(verse.text + "\n")


        verses_format.append("\n\nRead from the website: \n" + full_request)
        if len(verses_format) > 2000:
            error_message = "It looks like you're reading a Bible verse that has more than 2000 characters. Read instead from the website: \n" + full_request
            return error_message


        return "".join(verses_format)
