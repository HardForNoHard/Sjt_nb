import requests #请求
import re #正则
from google.protobuf import text_format
import dm_pb2
import sys 
import json 
from datetime import datetime

def get_cid(bvid, headers): #获取cid
    api_url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            return data['data']['cid']
        else:
            print(f"Error getting CID: {data['message']}")
            sys.exit(1)
    else:
        print(f"Error fetching CID: HTTP {response.status_code}")
        sys.exit(1)

def fetch_danmaku(cid, date, headers, output_file):
    content_list = []
    url = f'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={cid}&date={date}'
    print(f"Request URL: {url}")
    
    referer = f'https://www.bilibili.com/video/{bvid}/'
    headers['referer'] = referer
    print(f"Request Headers: {headers}")

    response = requests.get(url, headers=headers)
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        danmaku_data = dm_pb2.DmSegMobileReply()
        data = response.content
        danmaku_data.ParseFromString(data)
        for i in danmaku_data.elems:
            parse_data = text_format.MessageToString(i, as_utf8=True)
            try:
                progress = re.findall('progress:(.*)', parse_data)[0]
            except:
                progress = '1000'
            minutes, seconds = divmod(int(progress) // 1000, 60)
            content = re.findall('content:(.*)', parse_data)[0]
            content_list.append(f'{minutes:02d}:{seconds:02d} {content}')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_list))
        print("data has been saved")
    else:
        print(f"Error: {response.status_code}, Response Content: {response.content}")    
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python fetch_danmaku.py <bvid> <date> <headers_file> <output_file>")
        sys.exit(1)
    
    bvid = sys.argv[1]
    date = sys.argv[2]
    headers_file = sys.argv[3]
    output_file = sys.argv[4]

    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        sys.exit(1)

    with open(headers_file, 'r', encoding='utf-8') as f:
        headers = json.load(f)

    cid = get_cid(bvid, headers)
    print(f"Video CID: {cid}")

    fetch_danmaku(cid, date, headers, output_file)
