'''
运行此文件以读取教室列表，
请求每个教室的详细信息

生成 list.json 文件 - 教室列表
生成 details 文件夹 - 教室详细信息
'''


import requests
import json
import time
from os import getenv
from tqdm import tqdm

building_code_to_string = {
    "010102": "弘毅楼(附楼)",
    "010103": "弘毅楼(主楼)",
    "010106": "致远楼",

    "010201": "东教学楼",

    "020101": "爱特楼",
    "020102": "北教一",
    "020103": "北教二",
    "020104": "北教三",
    "020105": "学海楼",

    "020201": "博学北楼",
    "020202": "博学东楼",
    "020203": "博学西楼",
    "020204": "博学主楼",

    "030102": "教学大楼",
    "030201": "航海楼",
}

def request_list(domain, cookie, xnxqdm):
    url = f"https://{domain}/jwapp/sys/kcbcxby/modules/jskcb/jscx.do"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": cookie,
    }

    data = {
        "querySetting": '[{"name":"SFYPK","builder":"equal","linkOpt":"AND","value":"1"}]',
        "XNXQDM": xnxqdm,
        "*order": "+XXXQDM,+JXLDM,+JASMC",
        # "pageSize": getenv("PAGE_SIZE"),
        "pageSize": "841",
        "pageNumber": "1"
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.text)
    
    print(f"获取到{len(response.json()['datas']['jscx']['rows'])}条信息")

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    # write response to file
    with open('list.json', 'w', encoding='utf-8') as file:
        file.write(response.text)
        
def request_detail(classroom_code, domain, cookie, xnxqdm):
    url = f'https://{domain}/jwapp/sys/kcbcxby/modules/jskcb/jaskcb.do'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
    }
    data = {
        'XNXQDM': xnxqdm,
        'JASDM': classroom_code
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        # print('状态码:', response.status_code)
        # print('响应数据:', response.text)
        print(f"请求教室 {classroom_code} 成功")
    except Exception as e:
        print('请求失败:', e)

    # response = requests.post(url, headers=headers, data=data)

    # # 新建文件按照教室写到detail文件夹中
    # # 新建文件，名字是classroom_code
    with open(f"details/{classroom_code}.json", 'w', encoding='utf-8') as file:
        file.write(response.text)
        
    
    
    
def get_detail(domain, cookie, xnxqdm):
    with open('list.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    rows = data.get("datas", {}).get("jscx", {}).get("rows", [])
    
    rows.reverse()
    
    building_code_keys = building_code_to_string.keys()
    
    for row in tqdm(rows, desc="Processing: "):
        code = row.get("JASDM")
        if code[:6] not in building_code_keys:
            continue
        
        request_detail(code, domain, cookie, xnxqdm) 
        time.sleep(0.5)
        
    
    
    
if __name__ == "__main__":
    domain = getenv("JWXT_DOMAIN") or "jwxt.whut.edu.cn"
    cookie = getenv("COOKIE") or ""
    xnxqdm = getenv("XNXQDM") or "2025-2026-2"
    request_list(domain, cookie, xnxqdm)
    get_detail(domain, cookie, xnxqdm)
    # request_detail('0101020101', domain, cookie, xnxqdm)