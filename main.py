import asyncio
import time


from fetch import crawl_product


province_codes = [i for i in range(1, 65) if i != 20]

async def run_limit_worker(tasks, limit: int = 100):
    semaphore = asyncio.Semaphore(limit)

    async def sem_task(task):
        async with semaphore:
            return await task

    await asyncio.gather(*(sem_task(task) for task in tasks))
        

max_students_each_province = 108700
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