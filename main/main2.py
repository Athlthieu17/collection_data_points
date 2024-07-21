import asyncio
import time
from max_student import max
from fetch import crawl_product


province_codes = [i for i in range(3, 10) if i != 20]

async def run_limit_worker(tasks, limit: int = 100):
    semaphore = asyncio.Semaphore(limit)

    async def sem_task(task):
        async with semaphore:
            return await task

    for future in asyncio.as_completed([sem_task(task) for task in tasks]):
        result = await future
        yield result  # Yield the result of the completed task
        
        
# //108700
# max_students_each_province = 10
async def run_all_workers():
    tasks = []
    for province_code in province_codes:
        error_sbd = []
        with open(f'./output3/{province_code}_output.csv', 'w', encoding='utf8') as f:
            csv_header = 'sbd, toan, ngu_van, ngoai_ngu, vat_li, hoa_hoc, sinh_hoc, lich_su, dia_li, gdcd, ma_nn\n'
            f.write(csv_header)
            print('Start')
            print(f'--------------------------------------------{province_code}---------------------------')
            if province_code in range(1, 10):
                start_sbd = int('0' + str(province_code) + '0' * 6)
            else:
                start_sbd = int(str(province_code) + '0' * 6)
            end_sbd = start_sbd + int(max[province_code])
            products = []
            for sbd in range(int(start_sbd), int(end_sbd) + 1):
                # Chuyển đổi sbd sang chuỗi và thêm 0 nếu cần thiết
                sbd_str = str(sbd)
                if len(sbd_str) == 7:
                        sbd_str = "0" + sbd_str
                products.append(sbd_str)
            for product in products:
                task = crawl_product(product)
                tasks.append(task)

            async for result in run_limit_worker(tasks, limit=100):
                if result['process']:
                    f.write(result['data'] + '\n')
                else:
                    error_sbd.append(result['data'])
                # You can also process the result here if needed

            # Clear tasks for the next province (if you have multiple provinces)
            tasks.clear()   
        with open('error_sbd2.txt', 'a') as f:
                    for x in error_sbd:
                        f.write(str(x) + '\n')

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(run_all_workers())
    end_time = time.time()
    print(end_time - start_time)