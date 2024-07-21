import aiohttp
import json
url_crawl = ['https://giaoducthoidai.vn/tra-cuu-diem-thi.html', 'https://vtv.vn/tra-cuu-diem-thi-thpt.htm']
from useragent import UserAgent
import random

async def crawl_product(sbd) -> dict:
    headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "User-Agent": random.choice(UserAgent)
    }
    url = "https://vtvapi3.vtv.vn/handlers/timdiemthi.ashx?keywords=" + str(sbd)
    async with aiohttp.ClientSession() as client:
        try:
            async with client.get(url, headers=headers) as response:
                response.raise_for_status()  # Raise an exception for non-2xx status codes
                data = await response.text()
                data = json.loads(data)[0]

                if not data:  # Check for empty response
                    return {'process': 0, 'data': sbd}

                # Extract scores, assuming the data structure remains consistent
                record = ",".join([str(data[key]) for key in ['SOBAODANH', 'TOAN', 'VAN', 'NGOAI_NGU', 'LY', 'HOA', 'SINH', 'SU', 'DIA', 'GIAO_DUC_CONG_DAN', 'MA_MON_NGOAI_NGU']])
                return {'process': 1, 'data': record}

        except (aiohttp.ClientError, json.JSONDecodeError) as e:  # Handle specific exceptions
            return {'process': 0, 'data': sbd}

        except Exception as e:  # Catch unexpected errors
            return {'process': 0, 'data': sbd}
        #     r = await client.get(url, headers = headers)
        #     data = await r.text()
        #     data = json.loads(data)[0]
        #     record = \
        #                 data['SOBAODANH'] + ',' + \
        #                 data['TOAN'] + ',' + \
        #                 data['VAN'] + ',' + \
        #                 data['NGOAI_NGU'] + ',' + \
        #                 data['LY'] + ',' + \
        #                 data['HOA'] + ',' + \
        #                 data['SINH'] + ',' + \
        #                 data['SU'] + ',' + \
        #                 data['DIA'] + ',' + data['GIAO_DUC_CONG_DAN'] + ',' + data['MA_MON_NGOAI_NGU']
        #     return {'process':1, 'data': record}
        # except Exception as e:
        #     return {'process':0, 'data': sbd}