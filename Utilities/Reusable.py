def splitString(textstring, operator):
    split = textstring.split(operator)
    return split

def getRating(textstring):
    di = list(filter(str.isdigit, textstring))
    index = textstring.find(di[0])
    return (textstring[0:index], textstring[index : len(textstring)])
