import asyncio
import time
from max_student import max
from fetch import crawl_product


province_codes = [i for i in range(16, 29) if i != 20]

async def run_limit_worker(tasks, limit: int = 100):
    semaphore = asyncio.Semaphore(limit)

    async def sem_task(task):
        async with semaphore:
            return await task

    for future in asyncio.as_completed([sem_task(task) for task in tasks]):
        result = await future
        yield result  # Yield the result of the completed task
        

with open('D:/collection_data_points/error_sbd4.txt', 'r') as f:
    error_sbds = f.readlines()
                       
potential_recoverable_sbds = []

for sbd in error_sbds:
    # Remove any leading or trailing whitespace
    sbd = sbd.strip()

    # Check if the SBD format is valid (7-digit number)
    if len(sbd) == 8 and sbd.isdigit():
        # Add the SBD to the potential recoverable list
        potential_recoverable_sbds.append(str(sbd))
    else:
        potential_recoverable_sbds.append('0'+str(sbd))
        
        
async def run_all_workers():
    tasks = []
    # for province_code in province_codes:
    error_sbd = []
    with open(f'./output_2.csv', 'w', encoding='utf8') as f:
            csv_header = 'sbd, toan, ngu_van, ngoai_ngu, vat_li, hoa_hoc, sinh_hoc, lich_su, dia_li, gdcd, ma_nn\n'
            f.write(csv_header)
            products = []
            for sbd in potential_recoverable_sbds:
                products.append(sbd)
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
    with open('error_sbd5.txt', 'a') as f:
                    for x in error_sbd:
                        f.write(str(x) + '\n')

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(run_all_workers())
    end_time = time.time()
    print(end_time - start_time)