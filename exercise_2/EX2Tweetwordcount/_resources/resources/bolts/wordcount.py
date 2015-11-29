from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import psycopg2


class WordCounter(Bolt):
    def initialize(self, conf, ctx):
        self.counts = Counter()
        self.conn = psycopg2.connect(database="Tcount", user="postgres", password="postgres", host="localhost", port="5432")
        cur = self.conn.cursor()
        cur.execute("SELECT word, count from Tweetwordcount")
        for (key, count) in cur.fetchall():
            self.counts[key] = count
        self.conn.commit()

    def process(self, tup):
        word = tup.values[0]

        # Write codes to increment the word count in Postgres
        # Use psycopg to interact with Postgres
        # Database name: Tcount 
        # Table name: Tweetwordcount 
        # you need to create both the database and the table in advance.

        # Increment the local count
        self.counts[word] += 1
        self.emit([word, self.counts[word]])

        # myan: insert or update, depending on how many counts there are
        cur = self.conn.cursor()
        if self.counts[word] == 1:
            cur.execute("INSERT INTO Tweetwordcount (word,count) VALUES ('{text}', 1)".format(text=word))
        else:
            cur.execute("UPDATE Tweetwordcount SET count={count} WHERE word='{word}'".format(word=word, count=self.counts[word]))
        self.conn.commit()

        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))
