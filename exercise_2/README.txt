This is a step-by-step guide to run the Twitter streaming application for W205 exercise 2.

This guide assumes a user starts a fresh instance from ucbw205_complete_plus_postgres_PY2.7.

1. Install Python 2.7 and change python version to 2.7
$ sudo yum install python27-devel -y
$ mv /usr/bin/python /usr/bin/python266
$ ln -s /usr/bin/python2.7 /usr/bin/python

Check python version is 2.7.3
$ python --version

2. Install ez_setup and pip:
$ sudo curl -o ez_setup.py https://bootstrap.pypa.io/ez_setup.py
$ sudo python ez_setup.py
$ sudo /usr/bin/easy_install-2.7 pip
$ sudo pip install virtualenv

3. Install lein
$ wget --directory-prefix=/usr/bin/ https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein
$ chmod a+x /usr/bin/lein
$ sudo /usr/bin/lein
$ lein version

4. Install streamparse
$ pip install streamparse

5. Install the dependencies for the Twitter streaming application
$ pip install psycopg2
$ pip install tweepy
$ git clone https://github.com/tweepy/tweepy.git
$ cd tweepy
$ python setup.py install
$ cd ..

6. Configure postgres server settings

Initialize PostgresSQL
$ service postgresql initdb
$ sudo /etc/init.d/postgresql start

Edit the configurations
$ sudo vim /var/lib/pgsql/data/pg_hba.conf

Change:
local	all	all			ident
host	all	all	127.0.0.1/32	ident

To:
local	all	all			trust
host	all	all	0.0.0.0/0	md5

7. Restart the postgres server
$ sudo /etc/init.d/postgresql restart

8. Change the password for user 'postgres'
$ sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
$ sudo /etc/init.d/postgresql restart

9. Create database Tcount and table Tweetwordcount
Since the AMI is using PostgresSQL 8.4, which is fairly outdated version and which does not come with the functionality
to "CREATE TABLE IF NOT EXISTS", we decide to set up the database Tcount and table Tweetwordcount first.

$ sudo -u postgres createdb -O postgres Tcount
$ python
>>> import psycopg2
>>> conn = psycopg2.connect(database="Tcount", user="postgres", password="postgres", host="localhost", port="5432")
>>> cur = conn.cursor()
>>> cur.execute('''CREATE TABLE Tweetwordcount (word TEXT PRIMARY KEY NOT NULL, count INT NOT NULL);''')
>>> conn.commit()
>>> quit()

10. Checkout the code from Max's Github account and run application
$ git clone https://github.com/maxyan/UCB_MIDS_W205.git
$ cd UCB_MIDS_W205/exercise_2/EX2Tweetwordcount/
$ sparse run