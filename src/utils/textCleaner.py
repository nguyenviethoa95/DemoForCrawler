import re
import string

class Text_Cleaner:
    def __init__(self):
        self.input= None

    def cleanInput(self,input):
        input = re.sub('\n+'," ",input)
        input = re.sub('\[0-9]*\]',"",input)
        input = re.sub(' +'," ",input)
        input = bytes(input,"UTF-8")
        input = input.decode("ascii","ignore")
        cleanInput=[]
        input = input.split(' ')
        for item in input:
            # string.punctuation: list of all punctuation characters in Python
            # item.strip(punctuation) iterating through all words in the content, any punctuation character
            # on either side of word will be stripped.
            item= item.split(string.punctuation)
            if len(item)>1 or (item.lower() == 'a' or item.lower() =='i'):
                cleanInput.append(item)
        return cleanInput

    def ngrams(self, input, n):
        input= self.cleanInput(input)
        output=[]
        for i in range(len(input)-n+1):
            output.append(input[i:i+n])
        return output
