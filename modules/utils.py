
def id_from_mention(mentionStr):
    mentionStr = mentionStr.lstrip("<@")
    return mentionStr.rstrip(">")