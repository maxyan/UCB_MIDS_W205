import psycopg2
import re
import sys


def show_results(args):
    if len(args) == 1:
        # myan: python histogram.py 1,3
        start_count = int(args[0][0])
        end_count = int(args[0][2])
    elif len(args) == 2:
        # myan: python histogram.py 1, 3 or python histogram.py 1 3 or python histogram.py 1 ,3
        start_count = int(re.sub(",", "", args[0]))
        end_count = int(re.sub(",", "", args[1]))
    else:
        # myan: python histogram.py 1 , 3
        start_count = int(args[0])
        end_count = int(args[2])

    conn = psycopg2.connect(database="Tcount", user="postgres", password="postgres", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT word, count from Tweetwordcount where count>={start} AND count<={end}"
                .format(start=start_count, end=end_count))
    records = cur.fetchall()
    for (word, count) in records:
        print word + ": " + str(count) + "\n"
    conn.close()

if __name__ == "__main__":
    show_results(sys.argv[1:])


