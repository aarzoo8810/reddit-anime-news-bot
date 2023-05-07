#!venv/bin/python3
from bs4 import BeautifulSoup
import requests
import lxml
import os
from database import Database
from reddit import Reddit
import time

# this site doesn't send anything other than news data due to javascript
URL = "https://www.animenewsnetwork.com"
headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
	"Accept-Language": "en-US,en;q=0.5",
	"Connection": "keep-alive",
}
# do this project in class john watson rooney
reddit = Reddit()
database = Database()
database.create_table()


def insert_into_database(items: list):
	for row in items:
		url = row[0]
		url_exists = database.url_exists(url)

		if not url_exists:
			database.insert_row(row)
			print("added row:", row)
			if row[3] == "manga":
				reddit.post_anime_manga_news(title=row[1], url=row[0], thumbnail_url=row[2], is_manga=True)

				# sleep for 10 minutes , otherwise flagged as spam
				time.sleep(15*60)

			# below line comented out because r/anime will ban account if they flag it as a bot
			# else:
			# 	# reddit.post_anime_news(title=row[1], url=row[0], thumbnail_url=row[2])
			# 	pass


response = requests.get(URL, headers=headers)
print(f"{response}")
soup = BeautifulSoup(response.text, "lxml")

feeds = soup.find("div", class_="mainfeed-day")
news_boxes = feeds.find_all("div", class_="herald box news")

items = []
for news_box in news_boxes:
	title = news_box.find("h3").get_text().strip()
	news_url = news_box.h3.a.get("href")
	news_complete_url =  URL + news_url
	thumbnail_url = URL + news_box.find("div", class_="thumbnail").get("data-src")
	topic = news_box.find("span", class_="topics").get_text().strip()

	# some articles don't have topics tag if they don't generally relate to anime, manga, live-action
	if not topic:
		topic = None
	
	item = (news_complete_url, title, thumbnail_url, topic)
	items.append(item)


insert_into_database(items)