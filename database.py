import sqlite3


class Database:
	def __init__(self):
		self.con = sqlite3.connect("news.db")
		self.cur = self.con.cursor()

	def create_table(self):
		self.cur.execute("""CREATE TABLE IF NOT EXISTS news(
			url TEXT PRIMARY KEY,
			title TEXT,
			thumbnail_url TEXT,
			topic TEXT)""")

	def insert_row(self, row):
		self.cur.execute("""INSERT INTO news VALUES(?,?,?,?)""", row)
		self.con.commit()

	def read(self):
		self.cur.execute("""SELECT * FROM news""")
		rows = self.cur.fetchall()
		return rows

	def url_exists(self, url):
		url_exists = self.cur.execute("""SELECT * FROM news WHERE url=?""", (url,)).fetchone()
		if url_exists:
			return True