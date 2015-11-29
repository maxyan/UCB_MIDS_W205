#!/bin/bash

pip install streamparse
pip install psycopg2
pip install tweepy
git clone https://github.com/tweepy/tweepy.git
cd tweepy
python setup.py install
cd ..
