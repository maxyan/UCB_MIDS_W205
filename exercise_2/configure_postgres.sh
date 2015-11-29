#!/bin/bash

# Initialize PostgresSQL
service postgresql initdb
sudo /etc/init.d/postgresql start

# Override the postgres config file
cp -f ~/UCB_MIDS_W205/exercise_2/ /var/lib/pgsql/data/pg_hba.conf

# Some more setup work
sudo /etc/init.d/postgresql restart
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
sudo /etc/init.d/postgresql restart

# Setup database and tables
sudo -u postgres createdb -O postgres Tcount
cd ~/UCB_MID_W205/exercise_2
python set_up_db.py
cd ~
