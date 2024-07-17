import aiohttp
import json
url_crawl = ['https://giaoducthoidai.vn/tra-cuu-diem-thi.html', 'https://vtv.vn/tra-cuu-diem-thi-thpt.htm']

async def crawl_product(sbd) -> dict:
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
            record = \
                        data['SOBAODANH'] + ',' + \
                        data['TOAN'] + ',' + \
                        data['VAN'] + ',' + \
                        data['NGOAI_NGU'] + ',' + \
                        data['LY'] + ',' + \
                        data['HOA'] + ',' + \
                        data['SINH'] + ',' + \
                        data['SU'] + ',' + \
                        data['DIA'] + ',' + data['GIAO_DUC_CONG_DAN'] + ',' + data['MA_MON_NGOAI_NGU']
            # print(record)
            return record
        except Exception as e:
            return {"process": 'failed', 'sbd': sbd}