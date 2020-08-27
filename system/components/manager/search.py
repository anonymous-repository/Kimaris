from random import randint
# External Libraries
from fp.fp import FreeProxy
from proxyscrape import create_collector, get_collector, add_resource_type, get_proxyscrape_resource

# Manager
from components.manager.scholarly._scholarly import _Scholarly

def make_collector(page_i=''):
        http_collector = create_collector(f'http-collector-{page_i}', 'https')
        return http_collector

# Returns requests session with proxies (http, https)
def setup_new_proxies(http_collector):   
    
    proxy_http = http_collector.get_proxy()
    proxy_https = http_collector.get_proxy({'type':'https'})
    proxies={
        'http': f'http://{proxy_http.host}:{proxy_http.port}',
        'https' : f'https://{proxy_https.host}:{proxy_https.port}'
    }
    return proxies

try:
    http_collector = make_collector()
    resource_name = get_proxyscrape_resource(proxytype='http', timeout=5000, ssl='yes', anonymity='all', country='us') 
    add_resource_type('my-resource-type',resource_name)
except:
    pass


def set_new_proxy(scholar):
    global http_collector
    while True:
        http = setup_new_proxies(http_collector)
        print("Trying proxy:", http["http"], http["https"])
        proxy_works = scholar.use_proxy(http=http["http"], https=http["https"])
        if proxy_works:
            break
    print("Working proxy:", http["http"], http["https"])
    return http["https"]




def do_search2(search_string, type=0, n=10):
    
    scholar = _Scholarly()
    set_new_proxy(scholar)
    while True:
        try:
            search_ = scholar.search_pubs(search_string)
            break
        except:
            set_new_proxy(scholar)
    articles = []
    for _ in range(n):
        try:
            article = next(search_)
            articles.append(article)
            print(article)
        except:
            pass
    
    return articles

def do_search(search_string, type=0, n=10, captchas=True, steps=1):
    articles = []
    scholar = _Scholarly()
    #set_new_proxy(scholar)
    try:
        scholar.launch_tor('.\\Browser\\TorBrowser\\Tor\\tor.exe',4516,4517)
    except:
        pass
    if captchas:
        found = False
        while not found:
            try:
                search_ = scholar.search_pubs(search_string)
                article = next(search_).fill()
                print(article)
                articles.append(article)
                if article:
                    found = True
                    break
            except :
                #set_new_proxy(scholar)
                pass
            
    else: 
        set_new_proxy(scholar)
        while True:
            try:
                search_ = scholar.search_pubs(search_string)
                break
            except:
                set_new_proxy(scholar)
    
    for _ in range(n):
        try:
            article = next(search_)
            articles.append(article)
        except:
            pass
    
    return articles

def do_forward_step(article):
    cited_articles = []
    try:
        cited = article.citedby
        while True:
            try:
                cited_article = next(cited)
                cited_articles.append(cited_article)
                print(cited_article)
                print("cited")
            except:
                break
    except:
        print("Didnt get citedby")
        return []
    return cited_articles            
        