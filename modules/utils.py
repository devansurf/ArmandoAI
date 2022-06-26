import urllib

def id_from_mention(mentionStr):
    mentionStr = mentionStr.lstrip("<@")
    return mentionStr.rstrip(">")

def words_to_string(l, amount):
    dict_string = ""
    while len(l) < amount:
        amount -= 1

    for i in range(amount):
        dict_string = dict_string  + l[i][0] + ", "
    return dict_string 

def fetch(url):
    file = urllib.request.urlopen(url)
    words = []
    for line in file:
        decoded_line = line.decode("utf-8").rstrip("\n")
        if not decoded_line.startswith("#") and len(decoded_line) > 0:
            words.append(decoded_line)       
    return words

def fetch_profanity_words():
    url = "https://www.cs.cmu.edu/~biglou/resources/bad-words.txt"
    return fetch(url)
   

def fetch_preposition_words():
    url = "https://raw.githubusercontent.com/rali-udem/gophi/master/lexical-data/prepositions.txt"
    words = fetch(url)
    selectwords = ["a","i","is","the","it", "I", "I'm", "im"]
    for word in selectwords:
        words.append(word)
    return words
  