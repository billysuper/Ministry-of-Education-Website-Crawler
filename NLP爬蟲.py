import requests
from bs4 import BeautifulSoup
import json
import re

#def fetch_news_data(publisher, max_articles):
def fetch_news_data(unit,num_articles):
    news_items = [] 
    count = 0
    page = 0 
    size = 100
    while(count < num_articles):
        page += 1 # 下一頁
        url = f"https://www.edu.tw/News.aspx?n=9E7AC85F1954DDA8&page={page}&PageSize={size}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        for table in tables: 
            table_id = table.get('id')  # 提取table的id屬性
            if table_id=="ContentPlaceHolder1_gvIndex": # 找到公告欄
                trs = table.find_all('tr') # 提取所有公告
                for tr in trs:
                    trclasses = tr.get('class')
                    if isinstance(trclasses,list):
                        if('css_title' in trclasses): 
                            continue # 跳過欄位名稱
                        
                    tds = tr.find_all('td')
                    if tds[2].get_text(strip=True) != unit: # 查看單位
                        continue
                    As = tr.find_all('a')
                    for A in As:
                        a = A.get('href')
                    url = "https://www.edu.tw/" + a
                    respond = requests.get(url) # 取得公告內容頁面

                    # 使用Beautiful Soup解析HTML
                    soup = BeautifulSoup(respond.text, 'html.parser')

                    # 從<dd>標籤中提取文本
                    dd_text = soup.dd.get_text(separator=" ", strip=True)

                    # 提取資料，並處理可能缺失的項目
                    contact_person_match = re.search('聯絡人：(.*?)(?:\s|$)', dd_text)
                    contact_person = contact_person_match.group(1) if contact_person_match else "無"

                    phone_match = re.search('電話：(.*?)(?:\s|$)', dd_text)
                    phone = phone_match.group(1) if phone_match else "無" 

                    news_item = {
                        "date": tds[0].get_text(strip=True),
                        "unit": tds[2].get_text(strip=True),
                        "title": tds[1].get_text(strip=True),
                        "url": "https://www.edu.tw/" + a,
                        "author": {
                            "name": contact_person,
                            "tel": phone
                        }
                    }
                    news_items.append(news_item)
                    count += 1
                    print(f'取得第 {count:2} 筆資料')
                    if count >= num_articles: # 查看資料是否足夠
                        break
                break
    return news_items;

def main():
    try:
        num_articles = int(input("請輸入需爬取的文章數量: "))
        unit = input("請輸入需爬取的發布單位: ")
        
        news_items = fetch_news_data(unit, num_articles)
        
        # 轉換為JSON
        news_json = json.dumps(news_items, ensure_ascii=False, indent=4)

        # 將JSON字符串寫入文件
        with open('C:\\Users\\jungl\Desktop\\NLP\\news_data.json', 'w', encoding='utf-8') as f:
            f.write(news_json)
            print('蒐集完成')

    except ValueError:
        print("請輸入有效的數字")
    except Exception as e:
        print(f"發生程式錯誤: {e}")
    

if __name__ == "__main__":
    main()