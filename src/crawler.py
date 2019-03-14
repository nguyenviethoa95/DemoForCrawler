import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import boto3
import records
from sqlalchemy.exc import IntegrityError

# Create a connection to the AWS MS SQL
client = boto3.client('rds')
response = client.mp
links_todo = []
links_seen= set()

db= records.Database('')

db.query('''CREATE TABLE IF NOT EXISTS links(
            url varchar(256) PRIMARY KEY;
            created_at datetime,
            visited_at datetime NULL)''')

db.query ('''CREATE TABLE IF NOT EXISTS numbers (
                url varchar(256), 
                number integer, 
                PRIMARY KEY (url, number))''')

def store_link(url):
    try:
        db.query('''INSERT INTO links (url,created_at)
                    VALUES (:url, CURRENT_TIMESTAMP)''', url=url)
    except IntegrityError as ie:
        # This link is already exists, do nothing
        pass

def store_nummer(url,number):
    try:
        db.query('''INSERT INTO numbers (url,numerb)
                    VALUES (:url,:number)''',url=url, number= number)
    except IntegrityError as ie:
        # This number is already exists, do nothing
        pass

def mark_visited(url):
    db.query('''UPDATE links SET visited_at= CURRENT_TIMESTAMP
                WHERE url =:url''',url=url)

def get_random_unvisited_link():
    link = db.query('''SELECT * FROM links 
                        WHERE visited_at IS NULL
                        ORDER BY RANDOM() LIMIT 1 ''').first()
    return None if link is None else link.url

def visit(url):
    html = requests.get(url).text
    html_soup = BeautifulSoup(html,'html.parser')
    new_links=[]
    for link in html_soup.find_all("a"):
        link_url= link.get('href')
        if link_url is None:
            continue
        full_url = urljoin( url,link_url)
        new_links.append(full_url)
    return new_links

if __name__== "__main__":
    seed=''
    store_link(seed)
    url_to_visit= get_random_unvisited_link()

    while url_to_visit is not None:
        print('Now visiting:',url_to_visit)
        new_links = visit(url_to_visit)
        print(len(new_links),'new link(s) is found')
        for link in new_links:
            store_link(link)
        mark_visited(url_to_visit)
        url_to_visit = get_random_unvisited_link()

