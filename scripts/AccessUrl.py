import asyncio
from aiohttp import ClientSession
import re
from time import gmtime, strftime
import signal

class AccessUrl():
    def __init__(self, loop,file_in,file_out):
        self.loop = loop
        self.file_in = file_in
        self.file_out = file_out
        self.sem = asyncio.Semaphore(100)

        
    async def _fetch(self,url):
        #Use semaphore, too many urls processed concurrently may cause a crash
        async with self.sem:
            start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            str1 = start_time
            try:
                async with ClientSession(loop=self.loop) as sess:
                    response = await sess.get(url)
                    response = await response.text()
                    end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    str1 = str1 + " "+ url + " " + end_time
                    return str1,response
            except:
                end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                str1 = str1 + " "+ url + " " + end_time + " cannot connect"
                return str1, []
        
    async def _parse(self,url,expression):
        str1, html = await self._fetch(url)
        if "cannot connect" not in str1:
            x = re.findall(expression, html)
            return str1 + " " + str(x)
        else:
            return str1
        
    async def _write(self,url,expression):
        response = await self._parse(url,expression) 
        with open(self.file_out,"a") as f:
            f.write(response+'\n')

    async def __call__(self):
        with open(self.file_in) as fo:
            tasks = [self._write(line.split()[0],line.split()[1]) for line in fo]
        responses = await asyncio.gather(*tasks)
