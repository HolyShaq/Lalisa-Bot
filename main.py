import os
import random
import tweepy
import markovClass

# Authentication
consumerKey = ""
consumerSecret = ""
accessToken = ""
accessSecret = ""
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessSecret)
api = tweepy.API(auth)
print("\nTwitter authentication granted!")

# Get statuses from select fan accounts
print("Fetching sample tweets...")
userIDs = ["lisajpgs", "lalisarchive", "archivelisas", "lxsapics"]
tweets = []
for userID in userIDs:
    tweets.extend(api.user_timeline(id=userID, count=200))
    print(f"--Tweets from @{userID} fetched!")

# Loop through the tweets and append to "samples" list
samples = []
for text in [t.text for t in tweets]:

    # Filter out retweets, replies, and tweets that are possibly unrelated to Lisa (VERY HARDCODED, SORRY!)
    valid = True
    blacklists = ["RT", "@", "       ",  "thank you", "website", "somi"]
    for tag in blacklists:
        if tag in text:
            valid = False
            break
    if valid:
        # Boil down text to a list
        words = []
        for line in text.split("\n"):
            for word in line.split(" "):
              words.append(word)

        # Remove irrelevant parts of text
        for word in words[:]:
            if "https://t.co/" in word or "#" in word:
                words.remove(word)

        text = " ".join(words)
        if text == "" or len(text) > 90:
            pass
        else:
            samples.append(text+" (end)")

# Set up Markov Chain n-grams
print("Initializing n-gram dictionary...")
markov = markovClass.MarkovChain()
markov.learn(samples)

# Generate a tweet that hasn't been already posted
existingTweets = [t.text for t in api.user_timeline(count=200)]
while True:
    tweet = markov.generate()
    if tweet not in existingTweets:
        break

# Choose a random picture that hasn't been already posted
with open("existingImages.txt", "r") as file:
    existingImages = file.read().split("\n")
while True:
    img = random.choice(os.listdir("Picture Pool"))
    if img not in existingImages:
        break

# Post tweet with the chosen picture
api.update_with_media(f"Picture Pool/{img}", status=tweet)
print("\nPosted a tweet with the caption: ", tweet)
print("Image used: ", img)

# Append image code to existing images
with open("existingImages.txt", "a") as file:
    file.write(img + "\n")
