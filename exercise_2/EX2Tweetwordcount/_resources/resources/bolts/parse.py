from __future__ import absolute_import, print_function, unicode_literals
import re
from streamparse.bolt import Bolt

################################################################################
# Function to check if the string contains only ascii chars
################################################################################

LOW_VALUE_WORDS = ('i', 'me', 'my', 'you', 'your', 'yours', 'we', 'us', 'our', 'the', 'this', 'that',
                   'from', 'on', 'a', 'to', 'of', 'in', 'for', 'and', 'or', 'there', 'are', 'were',
                   'is', 'was', 'what', 'when', 'where', 'why', 'it', 'me', 'am', 'be', 'with', 'at', 'u',
                   'but', 'do', 'dont', 'can', 'cant', 'im', 'its', 'not', 'how', 'if', 'who', 'whom',
                   'whose', 'an', 'by', 'all', 'not', 'as', 'out', 'them', 'so', 'Ill', 'he', 'his', 'him',
                   'she', 'her', 'hers', 'they', 'them', 'their', 'theirs', 'been', 'really', 'youre',
                   'had', 'have', 'having')

def ascii_string(s):
    return all(ord(c) < 128 for c in s)


class ParseTweet(Bolt):
    def process(self, tup):
        tweet = tup.values[0]  # extract the tweet

        # Split the tweet into words
        words = tweet.split()

        # Filter out the hash tags, RT, @ and urls
        valid_words = []
        for word in words:

            # Filter the hash tags
            if word.startswith("#"): continue

            # Filter the user mentions
            if word.startswith("@"): continue

            # Filter out retweet tags
            if word.startswith("RT"): continue

            # Filter out the urls
            if word.startswith("http"): continue

            # Strip leading and lagging punctuations
            # myan: also strip all non-alphanumeric
            aword = re.sub(r'\W+', '', word.strip("\"?><,'.:;)"))

            # myan: filter out words that are too common words (i.e. without much meaning)
            # myan: a better way to do this is by using a dictionary. But this will work for now.
            if aword.lower() in LOW_VALUE_WORDS: continue

            # now check if the word contains only ascii
            if len(aword) > 0 and ascii_string(word):
                valid_words.append([aword])

        if not valid_words: return

        # Emit all the words
        self.emit_many(valid_words)

        # tuple acknowledgement is handled automatically
