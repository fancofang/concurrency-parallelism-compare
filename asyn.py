import os
import time
import asyncio
import aiohttp

BASE_URL = 'http://flupy.org/data/flags'
POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()
BASE_FILE = os.path.join(os.path.dirname(__name__),'downloads/')


async def get_flag(session,cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL,cc=cc.lower())
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
        for cc in POP20_CC:
            task = asyncio.create_task(download_one(session,cc))
            tasks.append(task)
        await asyncio.wait(tasks)

if __name__ == "__main__":
    start = time.time()
    asyncio.run(download_many())
    print(f'Time spending: {time.time()-start:0.2f}s')