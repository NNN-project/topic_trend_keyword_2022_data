import requests
from bs4 import BeautifulSoup
import pandas as pd
# import pymysql

#데이터베이스 연동
# conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='test', charset='utf8')
# cursor = conn.cursor()

#언론사 url 정보
press_ID = {"KBS":["355","121"], "MBC":["370","125"], "MBN":["74e","130"], "YTN":["5ae","129"], "SBS":["371","126"],
            "TV조선":["750","160"], "연합뉴스TV":["74f","161"], "채널A":["74b","159"], "JTBC ":["742","157"],
            "한국경제TV":"https://news.naver.com/main/tv/list.naver?mode=LPOD&mid=tvh&oid=215"}


def naver_news(day):
    #수집할 날짜
    day = day.replace("-", "")

    titles = []
    press = []
    dates = []

    for k, v in press_ID.items():
        # print(k)
        page_num = 0
        
        if k != "한국경제TV":
            for num in range(1, 30):
                url = f"https://news.naver.com/main/tv/list.naver?mode=LPOSD&mid=tvh&sid2={v[0]}&sid1={v[1]}&date={day}&page={num}"
                headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
                # print(url)
                #html불러오기
                original_html = requests.get(url, headers=headers)
                soup = BeautifulSoup(original_html.text, "html.parser")

                news = soup.find("ul", "type06").find_all("li")
                page = soup.find("div", "paging").find_all('a')
                
                #페이지 넘버 체크
                if len(page) > 0 and page[-1].get_text().isdigit():
                    if int(page[-1].get_text()) > page_num:
                        page_num = int(page[-1].get_text())
                elif len(page) == 0 and page_num == 0:
                    page_num = 1
                elif len(page) == 1 and page[-1].get_text() =='이전':
                    page_num = "stop"
                    
                #뉴스 정보 추출
                for i in news:
                    title = i.select_one("dl > dt:nth-of-type(2) > a").get_text()
                    title = title.replace("'", " ")
                    writing = i.find("span", "writing").get_text()
                    date = i.find("span","date").get_text().strip()
                    titles.append(title)
                    press.append(writing)
                    dates.append(date)
                    # cursor.execute(f"INSERT INTO navernews (title, press, c_date) VALUES ('{title.lstrip()}', '{writing}', '{date}')")
                
                #한페이지 뉴스 개수가 5개이하 이거나 페이지넘버가 num과 같을 때
                if len(news) < 5 or page_num == num or page_num == "stop":
                    break

        else:
            for num in range(1, 30):
                url = f"{v}&date={day}&page={num}"
                headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
                # print(url)
                #html불러오기
                original_html = requests.get(url, headers=headers)
                soup = BeautifulSoup(original_html.text, "html.parser")

                news = soup.find("ul", "type06").find_all("li")
                page = soup.find("div", "paging").find_all("a")
                
                #페이지 넘버 체크
                if len(page) > 0 and page[-1].get_text().isdigit():
                    if int(page[-1].get_text()) > page_num:
                        page_num = int(page[-1].get_text())
                elif len(page) == 0 and page_num == 0:
                    page_num = 1
                elif len(page) == 1 and page[-1].get_text() =='이전':
                    page_num = "stop"
                        
                #뉴스정보추출
                
                for i in news:
                    title = i.select_one("dl > dt:nth-of-type(2) > a").get_text()
                    title = title.replace("'", " ")
                    writing = i.find("span", "writing").get_text()
                    date = i.find("span","date").get_text().strip()
                    titles.append(title)
                    press.append(writing)
                    dates.append(date)
                    # cursor.execute(f"INSERT INTO navernews (title, press, c_date) VALUES ('{title.lstrip()}', '{writing}', '{date}')")
                
                #한페이 뉴스개수가 10개이하 이거나 페이지넘버가 num과 같을 때
                if len(news) < 10 or page_num == num or page_num == "stop":
                    break

    df = pd.DataFrame({
      "title" : titles, "press": press, "c_date": dates
      })

    return df

                
#데이터베이스에 commit하기
# conn.commit()

# 데이터베이스 연결을 닫습니다
# conn.close()