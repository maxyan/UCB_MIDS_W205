import psycopg2
import sys


def print_arguments(input_word):
    conn = psycopg2.connect(database="Tcount", user="postgres", password="postgres", host="localhost", port="5432")
    cur = conn.cursor()

    if input_word:
        cur.execute("SELECT word, count from Tweetwordcount where word='{word}'".format(word=input_word[0]))
        records = cur.fetchall()
        count = records[0][1] if records else 0
        print "Total number of occurrences of '{word}': {count}".format(word=input_word[0], count=count)
    else:
        cur.execute("SELECT word, count from Tweetwordcount")
        records = cur.fetchall()
        print records

    conn.close()


if __name__ == "__main__":
    print_arguments(sys.argv[1:])
