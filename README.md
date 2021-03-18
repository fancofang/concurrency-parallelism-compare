本测试的主要目的是对比python在并发和并行下的程序执行速度，希望能够给以后coding和模块选择提供参考。

样例代码是参考自《Fluent Python》。

<br/>

按照类型和模块，将代码分成5种，分别是：

1. 常规顺序执行（或者说是同步模式、普通模式）
2. 多进程模块`Multiprocessing`
3. 多线程模块`Multithreading`
4. 异步模块`asyncio`
5. 并行`cocurrent.future`模块

<br/>

# 代码展示

### 1. 常规顺序执行

在编程时候最常使用的方式。所有代码都会按照我们在编写时的思路按序依次执行。毫无疑问，这种方式是单线程，会堵塞，所以执行效率是最慢的。

代码如下

```
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
    image = get_flag(i)
    print(i, image)
    save_image(i,image)

def download_many(l):
    for i in l:
        download_one(i)

if __name__ == "__main__":
    start = time.time()
    download_many(POP20_CC)
    print(f'Time spending: {time.time()-start:0.2f}s')
```

<br/>

### 2. 多进程模块`Multiprocessing`

代码

```
from multiprocessing import Pool
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
    image = get_flag(i)
    print(i, image)
    save_image(i,image)

def download_many(l):
    with Pool(30) as p:
        res = p.map(download_one,l)

if __name__ == "__main__":
    start = time.time()
    download_many(POP20_CC)
    print(f'Time spending: {time.time()-start:0.2f}s')
```

<br/>

### 3. 多线程模块`Multithreading`

代码

```
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
```

<br/>

### 4. 异步模块`asyncio`

代码

```
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
```

<br/>

### 5. 并行`cocurrent.future`模块

`ProcessPoolExecutor`和 `ThreadPoolExecutor` 类都实现了通用的 Executor 接口，使用`concurrent.futures` 模块能实现processing和threading的方案，而且他们之间的转换也很容易。

所以这里会附上两个接口的代码。

processing接口代码如下

```
from concurrent.futures import ProcessPoolExecutor
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
    image = get_flag(i)
    print(i, image)
    save_image(i,image)

def download_many(l):
    with ProcessPoolExecutor() as executor:
        res = executor.map(download_one, sorted(l))
        
if __name__ == "__main__":
    start = time.time()
    download_many(POP20_CC)
    print(f'Time spending: {time.time()-start:0.2f}s')
```

threading接口代码如下：

```
from concurrent.futures import ThreadPoolExecutor
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
    image = get_flag(i)
    print(i, image)
    save_image(i,image)

def download_many(l):
    with ThreadPoolExecutor(max_workers=10) as executor:
        res = executor.map(download_one, sorted(l))
        
if __name__ == "__main__":
    start = time.time()
    download_many(POP20_CC)
    print(f'Time spending: {time.time()-start:0.2f}s')
```

<br/>

# 速度比较

从上面的代码可知，本次测试的主要内容是打开国家链接，下载国旗至`downloads`文件夹中。

测试的数据分为20个国家和全部国家（194个）两部分。每种代码都会各跑5次，取最低值，平均值，最高值。

* 由于请求速度非常快，为避免令`flupy`服务器认为是DoS攻击，所以测试全部国家的部分会在自行搭建的服务器中测试（已提供docker镜像）。不建议在`flupy`服务器上进行测试。

### 低数据量测试

测试下载20个国家的国旗

|                   | 1     | 2     | 3     | 4     | 5     | Min   | Max   | Average |
| ----------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ------- |
| 普通              | 19.95 | 22.96 | 35.15 | 24.16 | 39.45 | 19.95 | 39.45 | 28.334  |
| asyncio           | 1.66  | 3.92  | 0.99  | 1.62  | 1.31  | 0.99  | 3.92  | 1.9     |
| processing        | 3.68  | 3.73  | 2.64  | 4.56  | 3.21  | 2.64  | 4.56  | 3.564   |
| threading         | 3.27  | 1.85  | 3.42  | 2.78  | 3.26  | 1.85  | 3.42  | 2.916   |
| cocurrent-process | 3.79  | 4.78  | 4.27  | 8.75  | 4.1   | 3.79  | 8.75  | 5.138   |
| cocurrent-thread  | 2.11  | 3.24  | 2.04  | 2.2   | 2.16  | 2.04  | 3.24  | 2.35    |

从对比可知，并行和并发的方式基本比普通的执行方式快了10倍。无论选择进程、线程或是异步，效果都很显著。

### 高数据量测试

测试下载194个国家的国旗

|                   | 1     | 2     | 3     | 4     | 5     | Min   | Max   | Average |
| ----------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ------- |
| 普通              | 22.12 | 21.27 | 18.67 | 19.05 | 26.07 | 18.67 | 26.07 | 21.436  |
| asyncio           | 6.05  | 2.39  | 3.97  | 2.51  | 2.15  | 2.15  | 6.05  | 3.414   |
| processing        | 4.19  | 3.7   | 3.24  | 3.35  | 3.68  | 3.24  | 4.19  | 3.632   |
| threading         | 1.88  | 2.62  | 1.8   | 1.99  | 2.05  | 1.8   | 2.62  | 2.068   |
| cocurrent-process | 3.69  | 4.84  | 4.45  | 4.12  | 4.18  | 3.69  | 4.84  | 4.256   |
| cocurrent-thread  | 2.78  | 3.5   | 2.76  | 3.84  | 3.86  | 2.76  | 3.86  | 3.348   |

从对比可知，无论选择进程、线程或是异步，效果都很显著。

另外，看完上一个低数据量的表再看看高数据量的表，可能会感觉下载20个和下载194个时间相差不大。原因是在于访问的服务器不同，如果是访问低数据量，普通模式下需下载194个国旗需耗时166.39秒。

<br/>

# 服务器搭建

使用docker搭建简易服务器

创建镜像：

进入`docker_server`文件夹，执行

```
docker build -t image_name .
```

运行容器：

```
docker run -d -p 8999:8999 --name container_name image_name
```

如果容器运行成功，现在服务器就已搭建完成。通过`服务器地址:8999`即能访问。