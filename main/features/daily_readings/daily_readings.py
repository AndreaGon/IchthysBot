import requests
from bs4 import BeautifulSoup
import json
import datetime
import pytz
import os
import threading

class DailyReadings:
    def __init__(self):
        self.timezone = pytz.timezone('Asia/Singapore')
        self.date_time = datetime.datetime.now()
        self.current_time = self.date_time.replace(tzinfo=self.timezone)
        self.current_month = "{:02d}".format(self.current_time.month)
        self.current_day = "{:02d}".format(self.current_time.day)
        self.current_year = str(self.current_time.year % 100)
        self.readings_url = "https://bible.usccb.org/bible/readings/" + self.current_month + self.current_day + self.current_year + ".cfm"

    def dailyReadings(self):
        response = requests.get(self.readings_url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        readings_info = ["Taken from: " + self.readings_url]
        readings_content = soup.find_all('div', class_='wr-block b-verse bg-white padding-bottom-m')

        for reading in range(len(readings_content)):
            readings_info.append(readings_content[reading].text)
        return readings_info


