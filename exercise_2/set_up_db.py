import psycopg2


def set_up_db_table():    
	conn = psycopg2.connect(database="Tcount", user="postgres", password="postgres", host="localhost", port="5432")
	cur = conn.cursor()
	cur.execute('''CREATE TABLE Tweetwordcount (word TEXT PRIMARY KEY NOT NULL, count INT NOT NULL);''')
	conn.commit()
	conn.close()


if __name__ == "__main__":
    set_up_db_table()
