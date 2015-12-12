This is a step-by-step guide to run the Twitter streaming application for W205 exercise 2.

This guide assumes a user starts a fresh instance from ucbw205_complete_plus_postgres_PY2.7, check out the correct git repo, the user has root access, and starts from home directory (i.e. $ cd ~)

1. Checkout Max's git repo which contains the bash scripts and codes
$ git clone https://github.com/maxyan/UCB_MIDS_W205.git

Make all bash scripts executable
$ sudo chmod 777 ~/UCB_MIDS_W205/exercise_2/install_python_27.sh
$ sudo chmod 777 ~/UCB_MIDS_W205/exercise_2/install_dependencies.sh
$ sudo chmod 777 ~/UCB_MIDS_W205/exercise_2/configure_postgres.sh

2. Install the dependencies

Install Python 2.7
$ ./UCB_MIDS_W205/exercise_2/install_python_27.sh

Install lein (this step is a bit hard to automate as it requires keyboard input)
$ wget --directory-prefix=/usr/bin/ https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein
$ chmod a+x /usr/bin/lein
$ sudo /usr/bin/lein
$ lein version

Install other dependencies
$ ./UCB_MIDS_W205/exercise_2/install_dependencies.sh


3. Configure PostgresSQL
$ ./UCB_MIDS_W205/exercise_2/configure_postgres.sh

Create the table Tweetwordcount
$ cd UCB_MIDS_W205/exercise_2
$ python set_up_db.py


4. Run the application
$ cd EX2Tweetwordcount/
$ sparse run



Serving scripts
Below are some examples of the serving scripts.

$ cd ~/UCB_MIDS_W205/exercise_2/

$ python finalresults.py me
Total number of occurrences of 'me': 7

$ python finalresults.py me2345
Total number of occurrences of 'me2345': 0

$ python finalresults.py
[('women', 1), ('prove', 1), ('looked', 2), ('think', 2), ('pair', 1), ('Get', 1), ('gotta', 1), ('Thursday', 1), ('everyone', 1), ('man', 1), ('amp', 6), ('January', 1), ('wrong', 1), ('ready', 1), ('returns', 1), ('THIS', 1), ('98c', 1), ('FEAT', 1), ('hahahaha', 1), ('between', 1), ('respect', 1), ('calculator', 1), ('CW', 1), ('win', 4), ('reset', 1), ('disney', 1), ('21', 1), ('WATCH', 1), ('My', 4), ('now', 3), ('girl', 1), ('Building', 1), ('rounds', 1), ('has', 1), ('stronger', 1), ('He', 2), ('minds', 2), ('With', 1), ('scattering', 1), ('scatters', 1), ('can', 6), ('havent', 1), ('dumb', 1), ('way', 2), ('attitude', 2), ('favorite', 2), ('But', 1), ('your', 4), ('get', 6), ('posts', 1), ('into', 1), ('Tell', 1), ('tryna', 1), ('Gay', 1), ('JB', 1), ('concert', 1), ('Awww', 1), ('bibbity', 1), ('bobbity', 1), ('back', 1), ('like', 5), ('letters', 2), ('To', 2), ('fuck', 1), ('Extra', 1), ('Zone', 1), ('each', 1), ('watch', 1), ('directed', 1), ('the', 21), ('play', 1), ('her', 4), ('catch', 1), ('from', 1), ('Thats', 1), ('early', 1), ('priv', 1), ('awesome', 2), ('she', 3), ('sidelines', 1), ('season', 1), ('Hehe', 1), ('who', 2), ('doesnt', 1), ('relax', 1), ('turning', 1), ('Roswell', 2), ('arent', 1), ('Willie', 2), ('break', 2), ('about', 2), ('on', 6), ('if', 4), ('is', 8), ('winning', 1), ('bitch', 1), ('weak', 1), ('an', 4), ('few', 2), ('vent', 1), ('life', 5), ('sooo', 1), ('to', 19), ('wager', 1), ('more', 1), ('behind', 1), ('times', 1), ('ego', 1), ('just', 6), ('all', 3), ('One', 2), ('cute', 1), ('Thank', 1), ('sit', 1), ('How', 1), ('ended', 1), ('Win', 1), ('by', 2), ('far', 1), ('sharing', 1), ('going', 3), ('stupid', 1), ('His', 1), ('dumpling', 1), ('us', 2), ('ilysfm', 1), ('Were', 1), ('x13', 1), ('5', 1), ('lmao', 1), ('excitement', 1), ('crazy', 1), ('streets', 1), ('Tryna', 1), ('drink', 1), ('MAMA', 1), ('So', 1), ('you', 19), ('Lynch', 2), ('people', 4), ('completely', 2), ('road', 2), ('map', 2), ('at', 10), ('out', 3), ('You', 6), ('one', 3), ('will', 2), ('only', 5), ('cant', 3), ('event', 2), ('were', 4), ('PCs', 2), ('for', 8), ('up', 5), ('New', 2), ('Its', 3), ('first', 5), ('i', 5), ('Im', 5), ('mental', 2), ('he', 2), ('but', 3), ('want', 2), ('it', 7), ('corrupt', 2), ('are', 3), ('of', 13), ('less', 2), ('brand', 2), ('please', 3), ('and', 12), ('in', 10), ('so', 6), ('go', 2), ('perception', 2), ('dont', 2), ('The', 5), ('Just', 4), ('how', 4), ('two', 2), ('be', 6), ('its', 4), ('me', 7), ('have', 7), ('our', 7), ('A', 4), ('I', 12), ('boys', 1), ('should', 1), ('very', 1), ('well', 1), ('failed', 1), ('before', 1), ('almost', 1), ('ND', 1), ('rts', 1), ('100000', 1), ('choose', 1), ('lost', 1), ('M', 1), ('Direction', 1), ('players', 1), ('MA', 1), ('Country', 1), ('MinYoon', 1), ('right', 1), ('piece', 1), ('this', 7), ('next', 1), ('gain', 1), ('laid', 1), ('eyes', 1), ('What', 1), ('chair', 1), ('alternate', 1), ('Gentleman', 1), ('imagine', 1), ('helping', 1), ('beauty', 1), ('York', 1), ('Mino', 1), ('emotional', 2), ('letting', 1), ('timeless', 1), ('Yoon', 1), ('City', 1), ('new', 1), ('artwork', 1), ('Learn', 2), ('As', 2), ('lot', 1), ('swept', 1), ('Leader', 1), ('hidden', 1), ('better', 3), ('wish', 1), ('lol', 1), ('We', 1), ('busy', 1), ('got', 1), ('somebody', 1), ('Ailiee', 1), ('attends', 1), ('lucky', 1), ('worldfamous', 1), ('talking', 1), ('glances', 1), ('im', 3), ('ordering', 1), ('bird', 1), ('partners', 2), ('Invest', 2), ('lion', 1), ('could', 1), ('tear', 1), ('Coach', 1), ('story', 2), ('boyfriend', 1), ('vocal', 1), ('do', 1), ('award', 1), ('Weight', 1), ('covers', 1), ('Sister', 1), ('Elizabeth', 1), ('If', 1), ('Details', 1), ('myself', 1), ('Software', 1), ('Development', 1), ('Manager', 1), ('create', 1), ('spacecpm', 1), ('complain', 1), ('Decrease', 1), ('wldnt', 1), ('72', 1), ('Vacation', 1), ('Rentals', 1), ('Lebron', 1), ('Boston', 1), ('hunting', 1), ('method', 1), ('big', 1), ('injury', 1), ('three', 1), ('might', 2), ('hype', 1), ('Nicole', 1), ('unfair', 1), ('Kidman', 1), ('they', 3), ('feel', 1), ('important', 1), ('REAL', 2), ('someone', 1), ('theyd', 2), ('IS', 1), ('most', 1), ('yesterday', 1), ('goodness', 2), ('magnificent', 1), ('with', 3), ('Christmas', 2), ('stop', 1), ('giving', 1), ('art', 1), ('basic', 1), ('youve', 2), ('previously', 2), ('youre', 3), ('When', 1), ('Lesbian', 2), ('Star', 2), ('again', 1), ('Time', 1), ('need', 2), ('Be', 1), ('Alive', 1), ('phases', 1), ('something', 1), ('still', 1), ('shop', 1), ('President', 1), ('album', 1), ('Obama', 1), ('veterans', 1), ('own', 1), ('homeless', 1), ('secrets', 1), ('Trump', 1), ('It', 2), ('persons', 1), ('wont', 2), ('disability', 1), ('Happy', 1), ('BPs', 2), ('good', 1), ('today', 2), ('Heart', 2), ('trip', 2), ('was', 2), ('lucy', 2), ('day', 4), ('shit', 4), ('best', 2), ('not', 2), ('christmas', 2), ('1000', 2), ('ever', 2), ('AngelGod', 2), ('invest', 2), ('texted', 2), ('look', 2), ('game', 3), ('Oh', 2), ('stans', 2), ('know', 2), ('means', 3), ('that', 8), ('knew', 2), ('Bless', 2), ('Hes', 2), ('tweet', 2), ('much', 2), ('what', 6), ('did', 3), ('anyway', 2), ('kind', 2), ('hear', 2), ('my', 13), ('anything', 1), ('thinking', 1), ('plans', 1), ('Stop', 2), ('doubting', 1), ('Been', 1), ('Rather', 1), ('phone', 1), ('rather', 1), ('die', 1), ('instead', 1), ('call', 2), ('texts', 1), ('staff', 1), ('host', 1), ('class', 1), ('Ive', 1), ('been', 1), ('using', 1), ('Vim', 1), ('2', 1), ('years', 1), ('mostly', 1), ('because', 1), ('figure', 1), ('even', 2), ('exit', 1), ('happening', 1), ('over', 2), ('smile', 1), ('Weeknd', 1), ('enough', 1), ('hour', 1), ('Tiller', 1), ('Post', 1), ('his', 1), ('Malone', 1), ('Kanye', 1), ('Tory', 1), ('chipotle', 1), ('ARE', 1), ('Lanez', 1), ('when', 7), ('Three', 1), ('Changed', 1), ('Jordan', 1), ('Fetty', 1), ('Wap', 1), ('family', 1), ('World', 1), ('Dang', 1), ('clingy', 1), ('holiday', 1), ('tradition', 1), ('any', 1), ('TD', 1), ('Now', 1), ('space', 1), ('Playing', 1), ('Brew', 1), ('yours', 1), ('Wedding', 1), ('dog', 2), ('stroll', 1), ('we', 1), ('other', 1), ('him', 1), ('peoples', 1), ('love', 5), ('girlfriend', 1), ('blueberries', 1), ('world', 1), ('Wayne', 1), ('kid', 1), ('Harry', 1), ('hes', 2), ('excuses', 1), ('trash', 1), ('make', 3), ('happen', 1), ('Question', 2), ('check', 1), ('phoneSIKE', 1), ('ate', 2), ('closet', 1), ('package', 2), ('left', 1), ('freak', 1), ('cause', 1), ('23', 1), ('hard', 1), ('special', 1), ('guy', 1), ('end', 1), ('s', 1), ('Blatt', 1), ('than', 1), ('winner', 1), ('sheep', 1), ('7', 1), ('Reduction', 1), ('Kenny', 1), ('Help', 1), ('Fat', 1), ('compliments', 1), ('needs', 1), ('whats', 1), ('attractive', 1), ('Hours', 1), ('THE', 1), ('EGG', 1), ('COMING', 1), ('BACK', 1), ('HOME', 1), ('compete', 1), ('these', 1), ('females', 1), ('had', 2), ('icon', 2), ('person', 2), ('Things', 2), ('ex', 1), ('tries', 1), ('hit', 1), ('Porn', 2), ('No', 1), ('really', 1), ('customers', 1), ('ones', 1), ('say', 1), ('theyre', 1), ('gonna', 2), ('a', 25), ('fed', 1), ('different', 1)]



$ python histogram.py 10, 30
the: 21

to: 19

you: 19

at: 10

of: 13

and: 12

in: 10

I: 12

my: 13

a: 25
