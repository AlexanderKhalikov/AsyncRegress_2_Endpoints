import os
import requests
from pprint import pprint
import time
import aiohttp
import asyncio

# define url1 and url2 here


# set path to a directoryWithRequests
url1 = ""
url2 = ""

directoryWithRequests = ''
headers = {'content-type': 'application/soap+xml'}


def syncCompareResp(wsdl1, wsdl2, requestFile):

    with open(directoryWithRequests + '\\' + requestFile, encoding='utf-8') as my_file:
        body = my_file.read()

    response1 = requests.post(wsdl1, data=body.encode('utf-8'), headers=headers)
    response2 = requests.post(wsdl2, data=body.encode('utf-8'), headers=headers)

    if len(response1.content) != len(response2.content):
        print('\n\t\t-------NEW REQUEST--------\n\n')
        pprint(response1.text)
        print('\n\t------\n')
        pprint(response2.text)


def syncedRegress():
    start = time.time()

    for file in os.listdir(directoryWithRequests):
        if file.find('_Request') != -1:
            syncCompareResp(url1, url2, file)

    print("Sync Regress took: {:.2f} seconds".format(time.time() - start))


async def postRequestForFirstURL(client, file):
    async with client.post(url=url1, data=file, headers=headers) as resp:
        return await resp.text()


async def postRequestForSecondURL(client, file):
    async with client.post(url=url2, data=file, headers=headers) as resp:
        return await resp.text()


async def asynchronousRequests():
    start = time.time()
    async with aiohttp.ClientSession() as client:
        for file in os.listdir(directoryWithRequests):
            if file.find('_Request') != -1:
                tasks = [
                    postRequestForSecondURL(client, file),
                    postRequestForSecondURL(client, file)
                ]
                await asyncio.wait(tasks)
                response1 = await postRequestForFirstURL(client, file)
                response2 = await postRequestForSecondURL(client, file)
                if len(response1) != len(response2):
                    print('\n\t\t-------NEW REQUEST--------\n\n')
                    pprint(response1)
                    print('\n\t------\n')
                    pprint(response2)
    print("ASync Regress took: {:.2f} seconds".format(time.time() - start))


if __name__ == '__main__':

    syncedRegress()
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(asynchronousRequests())
    ioloop.close()
