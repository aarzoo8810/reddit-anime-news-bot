import praw
from praw.models import InlineImage
import os
from dotenv import load_dotenv
import requests
import shutil


class Reddit:
	def __init__(self):
		load_dotenv()
		self.client_id = os.getenv("client_id")
		self.client_secret = os.getenv("secret")
		self.password = os.getenv("password")
		self.user_agent = os.getenv("user_agent")
		self.username = os.getenv("username")

		self.reddit = praw.Reddit(
			client_id = self.client_id,
			client_secret = self.client_secret,
			password = self.password,
			user_agent = self.user_agent,
			username = self.username,)

		print(self.reddit.user.me())

	def post_anime_manga_news(self, title, url, thumbnail_url, is_manga=False):
		# check if this is anime subreddit, currently using test for test
		subreddit_name = "anime"
		if is_manga:
			subreddit_name = "manga"

			# Add [NEWS]/[ART] at the beginning because of r/manga rule
			title = f"[NEWS] {title}"

		anime_subreddit = self.reddit.subreddit(subreddit_name)

		# in final version shorten this line
		anime_flair_choices = list(anime_subreddit.flair.link_templates.user_selectable())
		template_id = None

		if len(anime_flair_choices) > 0:
			template_id = next(x for x in anime_flair_choices if x["flair_text"] == "News")["flair_template_id"]

		thumbnail_file = self.download_thumbnail_img(thumbnail_url)

		# add flair_id=template_id, later
		# anime_subreddit.submit(title=title, inline_media=media, selftext=selftext) # add url=url
		submit_post = anime_subreddit.submit_image(title=title, image_path=thumbnail_file, flair_id=template_id)
		self.remove_thumnail(thumbnail_file)

		submission_id = submit_post.id
		post = self.reddit.submission(submission_id)
		reply_text = f"Source: {url}"
		post.reply(reply_text)



	def download_thumbnail_img(self, url):
		r = requests.get(url, stream=True)
		file_name = url.split("/")[-1]

		if r.status_code == 200:
			with open(file_name, "wb") as img_file:
				r.raw.decode_content = True
				shutil.copyfileobj(r.raw, img_file)

		return file_name

	def remove_thumnail(self, file_name):
		os.remove(file_name)


	def delete_post(self):
		my_submissions = self.reddit.redditor("Immediate-Trash-6617").submissions
		for submission in self.reddit.redditor("Immediate-Trash-6617").submissions.top(time_filter="week"):
			subreddit = submission.subreddit

			if subreddit == "test":
				submission.delete()
				print("deleted")



reddit = Reddit()
# reddit.delete_post()

