from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import pandas

ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

# read the csv file and get cities list:
df = pandas.read_csv('seed_gross_mittel_list.csv',sep=';',header=None,encoding='iso-8859-1')
seeds = df.iloc[:,[1]].values.tolist()

seed_link ={}


# Main function
def proxy_generator():
    # Retrieve latest proxies
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
          'ip':   row.find_all('td')[0].string,
          'port': row.find_all('td')[1].string
        })

    # Choose a random proxy
    proxy_index = random_proxy()
    proxy = proxies[proxy_index]
    n = 0
    for seed in seeds[:5]:
        n = n + 1
        print('-----------------------------------------------------------', seed)
        r = Request('https://www.google.com/search?q={0}+amtsblatt'.format(str(seed[0])))
        with urlopen(r) as response:
            the_page = response.read()
        soup = BeautifulSoup(the_page, 'lxml')
        raw = soup.find_all("div", class_='g', limit=10)
        raws_splitted = str(raw).split('?q=')
        cut_tails = []

        for i in raws_splitted:
            head, sep, tail = i.partition('">')
            cut_tails.append(head)

        remove_google_ad = []
        for url in cut_tails[1:]:
            head1, sep1, tail1 = url.partition('&amp')
            remove_google_ad.append(head1)

        # print(remove_google_ad)
        seed_link[str(seed[0])] = remove_google_ad

    r.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

    # Every 10 requests, generate a new proxy
    if n % 10 == 0:
        proxy_index = random_proxy()
        proxy = proxies[proxy_index]

        # Make the call
        try:
            my_ip = urlopen(r).read().decode('utf8')
        except: # If error, delete this proxy and find another one
            del proxies[proxy_index]
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]

    with open('test.csv', 'w') as f:
        for key in seed_link.keys():
            f.write("%s,%s\n" % (key, seed_link[key]))

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
  return random.randint(0, len(proxies) - 1)

proxy_generator()