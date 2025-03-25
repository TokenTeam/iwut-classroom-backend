# import requests
# import json

# url = "https://jwxt.whut.edu.cn/jwapp/sys/kcbcxby/modules/jskcb/jscx.do"

# headers = {
#     "Accept": "application/json, text/javascript, */*; q=0.01",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "Connection": "keep-alive",
#     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#     "Cookie": "GS_SESSIONID=97daad10a47b68040f0004b75a8278a6; EMAP_LANG=zh; THEME=indigo; _WEU=your_weu_value; route=your_route_value",
#     "Host": "jwxt.whut.edu.cn",
#     "Origin": "https://jwxt.whut.edu.cn",
#     "Referer": "https://jwxt.whut.edu.cn/jwapp/sys/kcbcxby/*default/index.do?THEME=indigo&EMAP_LANG=zh",
#     "Sec-Ch-Ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Microsoft Edge\";v=\"134\"",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "\"Windows\"",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
#     "X-Requested-With": "XMLHttpRequest"
# }

# data = {
#     "querySetting": json.dumps([{
#         "name": "SFYPK",
#         "builder": "equal",
#         "linkOpt": "AND",
#         "value": "1"
#     }]),
#     "XNXQDM": "2024-2025-2",
#     "*order": "+XXXQDM,+JXLDM,+JASMC",
#     "pageSize": "20",
#     "pageNumber": "1"
# }

# try:
#     response = requests.post(url, headers=headers, data=data)
#     print("Status Code:", response.status_code)
#     print("Response:", response.text)
# except requests.RequestException as e:
#     print("Request failed:", e)

import requests

url = "https://jwxt.whut.edu.cn/jwapp/sys/kcbcxby/modules/jskcb/jaskcb.do"

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "GS_SESSIONID=97daad10a47b68040f0004b75a8278a6; EMAP_LANG=zh; THEME=indigo; _WEU=your_weu_value; route=your_route_value",
    "Host": "jwxt.whut.edu.cn",
    "Origin": "https://jwxt.whut.edu.cn",
    "Referer": "https://jwxt.whut.edu.cn/jwapp/sys/kcbcxby/*default/index.do?THEME=indigo&EMAP_LANG=zh",
    "Sec-Ch-Ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Microsoft Edge\";v=\"134\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
    "X-Requested-With": "XMLHttpRequest"
}

data = {
    "XNXQDM": "2024-2025-2",
    "JASDM": "0101020101"
}

try:
    response = requests.post(url, headers=headers, data=data)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
except requests.RequestException as e:
    print("Request failed:", e)
