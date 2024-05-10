import asyncio
import time
import aiohttp
import json

province_codes = [i for i in range(1, 65) if i != 20]

async def run_limit_worker(tasks, limit: int = 100):
    semaphore = asyncio.Semaphore(limit)

    async def sem_task(task):
        async with semaphore:
            return await task

    await asyncio.gather(*(sem_task(task) for task in tasks))


async def crawl_product(sbd):
    headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "Referer": "https://vtv.vn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    url = "https://vtvapi3.vtv.vn/handlers/timdiemthi.ashx?keywords=" + str(sbd)
    async with aiohttp.ClientSession() as client:
        try:
            r = await client.get(url, headers = headers)
            data = await r.text()
            data = json.loads(data)[0]
            print(data)
        except Exception as e:
            print(f"Lỗi khác khi lấy dữ liệu cho SBD {sbd}: {e}")
        return None
        
        
        
            # todo: process your output here

max_students_each_province = 1000
async def run_all_workers():
    tasks = []
    for province_code in range (1,2):
        print('Start')
        print(f'--------------------------------------------{province_code}---------------------------')
        if province_code in range(1, 10):
            start_sbd = int('0' + str(province_code) + '0' * 6)
        else:
            start_sbd = int(str(province_code) + '0' * 6)
        end_sbd = start_sbd + max_students_each_province
        products = []
        for sbd in range(int(start_sbd), int(end_sbd) + 1):
            # Chuyển đổi sbd sang chuỗi và thêm 0 nếu cần thiết
            sbd_str = str(sbd)
            if len(sbd_str) == 7:
                    sbd_str = "0" + sbd_str
            products.append(sbd_str)
        print(products)
        for product in products:
            tasks.append(crawl_product(product))

    await run_limit_worker(tasks, limit=100)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(run_all_workers())
    end_time = time.time()
    print(end_time - start_time)