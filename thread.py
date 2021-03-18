import threading
import requests
import os
import time

BASE_URL = 'http://flupy.org/data/flags'
POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()
BASE_FILE = os.path.join(os.path.dirname(__name__),'downloads/')

def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL,cc=cc.lower())
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
    download_many(POP20_CC)
    print(f'Time spending: {time.time()-start:0.2f}s')