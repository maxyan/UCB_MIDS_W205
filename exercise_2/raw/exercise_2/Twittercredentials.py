import tweepy

consumer_key = "7zKulgQh8LNKDk6uv95LGJU9l";
#eg: consumer_key = "YisfFjiodKtojtUvW4MSEcPm";


consumer_secret = "3LMyLGqf29H7JiYfEysnThBAs1xwfwoGkyHuXLxWts8HeXj7JA";
#eg: consumer_secret = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";

access_token = "149939938-Meyglx1MDT9XQZttB2bSyVrcVtGlBtiZwI4Ct77E";
#eg: access_token = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";

access_token_secret = "SwvCFQycb86zpzlToNkYxJqHr6ytT4m7Up4p67JQsrtya";
#eg: access_token_secret = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



