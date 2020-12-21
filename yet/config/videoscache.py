import sqlite3 as sq
import datetime
import os
from pathlib import Path


class VideosCache(object):
    CACHE_PATH = os.path.join(Path.home(), ".cache", "yet")
    VIDEOS_CACHE_DB_PATH = os.path.join(CACHE_PATH, "videoscache.db")
    TABLE = "videos_cache"

    def __init__(self, clean_day=0):
        self._create_table_if_not_exists()
        if clean_day > 0:
            self.clear_old_cache(clean_day)

    def _create_table_if_not_exists(self):
        ''' Creates dir and sql table if not exists '''
        if not os.path.exists(self.CACHE_PATH):
            os.makedirs(self.CACHE_PATH)
        with sq.connect(self.VIDEOS_CACHE_DB_PATH) as connection:
            sql = 'create table if not exists ' + self.TABLE + \
                ' (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, link TEXT, date timestamp)'
            connection.execute(sql)

    def add_to_cache(self, url):
        if self.contains(url):
            return
        sql = 'INSERT INTO ' + self.TABLE + ' (link, date) values(?, ?)'
        values = (url, datetime.datetime.today())
        with sq.connect(self.VIDEOS_CACHE_DB_PATH) as connection:
            connection.execute(sql, values)

    def delete(self, url):
        if not self.contains(url):
            return
        sql = 'DELETE FROM ' + self.TABLE + ' WHERE link = ?'
        with sq.connect(self.VIDEOS_CACHE_DB_PATH) as connection:
            connection.execute(sql, (url,))

    def contains(self, url):
        sql = 'SELECT * FROM ' + self.TABLE + ' WHERE link = ?'
        with sq.connect(self.VIDEOS_CACHE_DB_PATH) as connection:
            data = connection.execute(sql, (url,))
            for row in data:
                return True
        return False

    def contains_all(self, urls):
        for url in urls:
            if not self.contains(url):
                return False
        return True

    def clear_cache(self):
        sql = 'DELETE FROM ' + self.TABLE + ';'
        with sq.connect(self.VIDEOS_CACHE_DB_PATH) as connection:
            connection.execute(sql)

    def clear_old_cache(self, days):
        sql = 'DELETE FROM ' + self.TABLE + ' WHERE date < ?'
        date = datetime.datetime.today() - datetime.timedelta(days=days)
        with sq.connect(self.VIDEOS_CACHE_DB_PATH) as connection:
            connection.execute(sql, (date,))
