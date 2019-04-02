from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.text_rank import TextRankSummarizer  as Summarizer
from sumy.utils import get_stop_words
import requests
from boto3.dynamodb.conditions import Attr
from src.baseclass import BotoClient
LANGUAGE = "german"
SENTENCES_COUNT = 10

class Text_Summarizer():

    def __init__(self,conn,table_name):
        self.conn= conn
        self.table= conn.Table(table_name)

    def get_next_link_to_visit(self):
        table = self.conn.Table('seeds')
        response = table.scan(
            FilterExpression= Attr('textrank').not_exists() & Attr('valid').eq(True),
        )
        result = len(response['Items'])
        return (None,None) if result == 0 else (response['Items'][0]['ID'], response['Items'][0]['url'])

    def mark_invalid(self,id):
        self.table.update_item(
            Key={
                'ID': str(id)
            },
            UpdateExpression="SET valid = :var1",
            ExpressionAttributeValues={
                ':var1': False,
            },
        )

    def mark_valid(self,id):
        self.table.update_item(
            Key={
                'ID': str(id)
            },
            UpdateExpression="SET valid = :var1",
            ExpressionAttributeValues={
                ':var1': True,
            },
        )

    def parse_html(self,id,url):
        if requests.head(url).status_code == 200:

            parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))

            if len(parser.document.sentences) != 0:
                # or for plain text files
                # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
                stemmer = Stemmer(LANGUAGE)

                summarizer = Summarizer(stemmer)
                summarizer.stop_words = get_stop_words(LANGUAGE)
                sen = []

                for sentence in summarizer(parser.document, SENTENCES_COUNT):
                    sen.append(str(sentence))

                text = '.'.join(sen)
                #print(text)
                text.replace(u'\n', '')
                self.mark_valid(id)
                return {'ID':str(id),'textrank':text}
            else:
                self.mark_invalid(id)
                return None
        else:
            self.mark_invalid(id)
            return None

    def put_object(self,id,text):
        self.table.update_item(
            Key={
                'ID': str(id)
            },
            UpdateExpression="SET textrank = :var1",
            ExpressionAttributeValues={
                ':var1': text,
            },
        )

    def start(self):
        id,url = self.get_next_link_to_visit()
        while url is not None:
           # print(id, url)
            obj= self.parse_html(id,url)
            if obj is not None:
                self.put_object(obj['ID'],obj['textrank'])
                print(url + 'is processed')
                id,url = self.get_next_link_to_visit()

if __name__ == "__main__":
    summarizer= Text_Summarizer(BotoClient.BotoClient('dynamodb').connect(), 'seeds')
    summarizer.start()