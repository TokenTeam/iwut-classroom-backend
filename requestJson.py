import requests
import json
import time
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

def request_list():
    url = "https://jwxt.whut.edu.cn/jwapp/sys/kcbcxby/modules/jskcb/jscx.do"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "GS_SESSIONID=e914e5dc620579c692953f64d2a7145f; EMAP_LANG=zh; THEME=indigo; _WEU=G9Bgp_bbia_ilvs0OAtb2cgfo7paVBlRgTq7YblQ8iyGlYPFp6vLS8cbNFnf*59AFD9_QnGlV3ic6iNAmRgbQz9xkaMvf_MSpYXv6eLP6v3mPH*hLY1lU*E05kfZbkmhI1xuOh9rzq8t50trV_cWxbeUNU79I8bJ024w*EZHCvs57LP1kVE5pVVHKm2gqZwjoFMkqfRrYKn1Kj8DssBClGD6L9dinrb2lsFN*aC05D1QiA9_UCrnxulXxxwfUsLa1DNnRGt8LP2kjFoK6MMetEkzEbZmfFlPyDk61FjlTsY7tQ9*kpGXwc..; route=3b67e13f5826924e7f04fda23e56535a",
        "host": "jwxt.whut.edu.cn",
        "origin": "https://jwxt.whut.edu.cn",
        "referer": "https://jwxt.whut.edu.cn/jwapp/sys/kcbcxby/*default/index.do?THEME=indigo",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }

    data = {
        "querySetting": '[{"name":"SFYPK","builder":"equal","linkOpt":"AND","value":"1"}]',
        "XNXQDM": "2024-2025-2",
        "*order": "+XXXQDM,+JXLDM,+JASMC",
        "pageSize": "844",
        "pageNumber": "1"
    }

    response = requests.post(url, headers=headers, data=data)
    
    print(f"获取到{len(response.json()['datas']['jscx']['rows'])}条信息")

    # print("状态码:", response.status_code)
    # print("响应内容:", response.text)
    # write response to file
    with open('list.json', 'w', encoding='utf-8') as file:
        file.write(response.text)
        
def request_detail(classroom_code):
    url = 'https://jwxt.whut.edu.cn/jwapp/sys/kcbcxby/modules/jskcb/jaskcb.do'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'connection': 'keep-alive',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'GS_SESSIONID=799e405060d965334dd823e701871f1f; EMAP_LANG=zh; THEME=indigo; _WEU=qi0dCwYr6ziRSOntxoHE9CSRwIUbAiRxsoghbBOzkA9CEHce6Yqi4Od4Dg8gcoR0FAOuEGBiDSenTqwiLKu4uMaMzDYCoWMHcLlQs2r*kxrwAf8hYuN*mERvKnkZQ7xhAxox2RtEdgXExpDZCtGc99Rzrztz7deMc3cf1qvymA_LV20QeJhlkjhfbyevNv2brOe_PRJME742b5OfKSxUG5uqhmdK5Sesu5FsBMjrGp9ZVRyCg3wfvj5KY4MMTk0XkRxNqFUjWr4VPOiP2kkATYEkc9om2hOpXQZ*MiGK_V1FeRbsrAejkxN3jyD0v4jm; route=4a18965ca556fcb9748ac4f96de97073',
        'origin': 'https://jwxt.whut.edu.cn',
        'referer': 'https://jwxt.whut.edu.cn/jwapp/sys/kcbcxby/*default/index.do?THEME=indigo&THEME_VARIABLES=&RADIUS=20&EMAP_LANG=zh&forceApp=kcbcxby&_yhz=00000ef212c48c8f84be79acbd9d81b090f51&min=1',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {
        'XNXQDM': '2024-2025-2',
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
        
    
    
    
def get_detail():
    with open('list.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    rows = data.get("datas", {}).get("jscx", {}).get("rows", [])
    
    rows.reverse()
    
    building_code_keys = building_code_to_string.keys()
    
    for row in tqdm(rows, desc="Processing: "):
        code = row.get("JASDM")
        if code[:6] not in building_code_keys:
            continue
        
        request_detail(code) 
        time.sleep(5)
        
    
    
    
if __name__ == "__main__":
    get_detail()
    # request_detail('0101020101')