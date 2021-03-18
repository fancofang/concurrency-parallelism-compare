import os
import time
import asyncio
import aiohttp

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


async def get_flag(session,cc):
    url = '{}/{cc}'.format(BASE_URL,cc=cc.lower())
    async with session.get(url) as resp:
        return await resp.read()

def save_image(cc,flow):
    with open(os.path.join(BASE_FILE, cc+'.gif'), mode='wb') as f:
        f.write(flow)

async def download_one(session, i):
    image = await get_flag(session,i)
    print(i, image)
    save_image(i,image)

async def download_many():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for cc in POPALL_CC:
            task = asyncio.create_task(download_one(session,cc))
            tasks.append(task)
        await asyncio.wait(tasks)

if __name__ == "__main__":
    start = time.time()
    asyncio.run(download_many())
    print(f'Time spending: {time.time()-start:0.2f}s')