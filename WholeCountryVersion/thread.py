import threading
import requests
import os
import time

BASE_URL = 'http://server_ip:8999/flags'
POPALL_CC = ['ad', 'ae', 'af', 'ag', 'al', 'am', 'ao', 'ar', 'at', 'au', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh',
            'bi', 'bj', 'bn', 'bo', 'br', 'bs', 'bt', 'bw', 'by', 'bz', 'ca', 'cd', 'cf', 'cg', 'ch', 'ci', 'cl', 'cm',
            'cn', 'co', 'cr', 'cu', 'cv', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'dz', 'ec', 'ee', 'eg', 'er', 'es', 'et',
            'fi', 'fj', 'fm', 'fr', 'ga', 'gb', 'gd', 'ge', 'gh', 'gm', 'gn', 'gq', 'gr', 'gt', 'gw', 'gy', 'hn', 'hr',
            'ht', 'hu', 'id', 'ie', 'il', 'in', 'iq', 'ir', 'is', 'it', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km',
            'kn', 'kp', 'kr', 'kw', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc',
            'md', 'me', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mr', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'ne',
            'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nz', 'om', 'pa', 'pe', 'pg', 'ph', 'pk', 'pl', 'pt', 'pw', 'py', 'qa',
            'ro', 'rs', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'ss',
            'st', 'sv', 'sy', 'sz', 'td', 'tg', 'th', 'tj', 'tl', 'tm', 'tn', 'to', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua',
            'ug', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vn', 'vu', 'ws', 'ye', 'za', 'zm', 'zw']
BASE_FILE = os.path.join(os.path.dirname(__name__),'downloads/')

def get_flag(cc):
    url = '{}/{cc}'.format(BASE_URL,cc=cc.lower())
    resp = requests.get(url)
    image = resp.content
    return image

def save_image(cc,flow):
    with open(os.path.join(BASE_FILE, cc+'.gif'), mode='wb') as f:
        f.write(flow)

def download_one(i):
    print('thread %s is running...' % threading.current_thread().name)
    image = get_flag(i)
    print(i, image)
    save_image(i,image)

def download_many(l):
    threads = list()
    for i in l:
        task = threading.Thread(target=download_one, name=i, args=(i,))
        threads.append(task)
        task.start()
        
    for thread in threads:
        thread.join()
        
if __name__ == "__main__":
    start = time.time()
    download_many(POPALL_CC)
    print(f'Time spending: {time.time()-start:0.2f}s')