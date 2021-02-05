import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_page_content(url):
    # 得到页面的内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
    html = requests.get(url, headers=headers, timeout=10)
    content = html.text
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def analysis(soup):
    temp = soup.find('div', class_="tslb_b")
    df = pd.DataFrame(columns=[
                      'id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
    tr_list = temp.find_all('tr')
    for tr in tr_list:
        td_list = tr.find_all('td')
        if len(td_list) > 0:
            id, brand, car_model, type, desc, problem, datetime, status = td_list[0].text, td_list[1].text, td_list[
                2].text, td_list[3].text, td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
            temp = {}
            temp['id'] = id
            temp['brand'] = brand
            temp['car_model'] = car_model
            temp['type'] = type
            temp['desc'] = desc
            temp['problem'] = problem
            temp['datetime'] = datetime
            temp['status'] = status
            df = df.append(temp, ignore_index=True)
    return df


result = pd.DataFrame(columns=[
                      'id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])

# 请求URL
base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'
page_num = 30
for i in range(page_num):
    request_url = base_url + str(i + 1) + '.shtml'
    soup = get_page_content(request_url)
    df = analysis(soup)
    result = result.append(df)

print(result)
result.to_csv('car_complain_xa.csv', index=False)
result.to_excel('car_complain_xa.xlsx', index=False)
# print(soup)
# 输出第一个 title 标签
# print(soup.title)
# # 输出第一个 title 标签的标签名称
# print(soup.title.name)
# # 输出第一个 title 标签的包含内容
# print(soup.title.string)
