import requests
from bs4 import BeautifulSoup
import json
import datetime
import pytz
import os

class Prayers:
    def readPrayer(self, prayer):
        with open("prayers.json") as f:
            prayers = json.load(f, strict=False)

        with open("prayers-latin.json") as f:
            prayers_latin = json.load(f, strict=False)
        print(prayer)
        if prayer in prayers:
            return prayers[prayer]
        elif prayer in prayers_latin:
            return prayers_latin[prayer]
        else:
            return "Prayer not found"
