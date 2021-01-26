import nest_asyncio
nest_asyncio.apply()

import time, ctypes
import asyncio, aiohttp

cookie = open('cookie.txt','r').readline().strip()

async def main():
    client = aiohttp.ClientSession()
    headers = {'X-CRSF-TOKEN': ''}
    cookies = {'.ROBLOSECURITY': cookie}

    success = 0
    sent_requests = 0

    async def thread():
        nonlocal success, sent_requests
        while sent_requests < 10000:
            try:
                async with client.post(f'https://economy.roblox.com/v1/purchases/products/{productid}', cookies=cookies, headers=headers, data={'expectedCurrency': 1, 'expectedPrice': 0, 'expectedSellerId': 1}, timeout=5) as resp:
                    r = await resp.text()
                if 'Success' in r: success += 1
                sent_requests += 1
            except:
                pass

    async with client.get('https://www.roblox.com/mobileapi/userinfo', cookies=cookies, timeout=5) as resp:
        r = str(resp.url)
    if 'mobileapi/user' not in r:
        input('Invalid Cookie.')
        exit()

    assetid = int(input('assetid: '))
    async with client.get(f'https://api.roblox.com/Marketplace/ProductInfo?assetId={assetid}', timeout=5) as resp:
        r = await resp.json()
    productid = r['ProductId']

    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.wait([thread() for i in range(250)]))

    async with client.post('https://auth.roblox.com/v2/login', cookies=cookies, timeout=5) as resp:
        r = resp.headers
    xcrsf = r['X-CSRF-TOKEN']

    start=time.time()
    await asyncio.sleep(3)
    headers = {'X-CSRF-TOKEN': xcrsf}
    while sent_requests < 10000:
        await asyncio.sleep(1)
        rps = round(sent_requests/(round(time.time()-start,2)))
        ctypes.windll.kernel32.SetConsoleTitleW(f'Purchased: {success} | Request sent: {sent_requests} | Requests per second: {rps}')    

asyncio.run(main())
input('Finished.')