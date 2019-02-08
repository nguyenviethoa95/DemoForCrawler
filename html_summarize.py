from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
#from sumy.summarizers.lsa import LsaSummarizer as Summarizer
#from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer

from sumy.utils import get_stop_words
import config
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from boltons.iterutils import remap
import requests
import time

LANGUAGE = "german"
SENTENCES_COUNT = 10

if __name__ == "__main__":
    # create conn to dynamodb
    session = boto3.Session(region_name=config.CURRENT_REGION,
        aws_access_key_id=config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],
        aws_secret_access_key=config.AWS_CONFIG['AWS_SERVER_SECRET_KEY'])
    table = session.resource('dynamodb').Table('url_cities')
    table1 = session.resource('dynamodb').Table('result_summarizer')
    response1= table.scan()
    keys =''
    for a in response1['Items']:
        keys =keys +' '+ a['ID']

    # scan the url_cities and get all items
    #fe = Key('ID')
    response = table.scan()
    items={}
    for i in response['Items']:
        items[i['ID']]= i['url']

    result=[]

    for i in items:

        url = items[i][0]
        print(url)
        doable=False

        try:
            t0 = time.time()
            requests.get(url)
            doable=True
        except Exception as x:
            print(x)
            doable=False
            t1 = time.time()
            print('Took', t1 - t0, 'seconds')

        if (doable== True and requests.head(url).status_code ==200):
            parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
            if len(parser.document.sentences) !=0:
                # or for plain text files
                # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
                stemmer = Stemmer(LANGUAGE)

                summarizer = Summarizer(stemmer)
                summarizer.stop_words = get_stop_words(LANGUAGE)
                sen = []

                for sentence in summarizer(parser.document, SENTENCES_COUNT):
                    sen.append(str(sentence))

                text ='.'.join(sen)
                text.replace(u'\n','')
                obj ={}
                obj['ID']= str(i)
                obj['TextRank']=text

                #drop_falsey = lambda path, key, value: bool(value)
                #clean = remap(obj, visit=drop_falsey)

                #output= json.dumps(clean,ensure_ascii=False).encode("utf-8")
                # write the result back into the table
                table =  session.resource('dynamodb').Table('result_summerizer')
                res = table.update_item(
                    Key={
                        'ID': str(i)
                    },
                    UpdateExpression="SET luhn = :var1",
                    ExpressionAttributeValues={
                        ':var1': text,
                    },
                )