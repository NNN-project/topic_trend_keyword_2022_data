# Topic_Trend_Keyword 데이터수집

네이버 뉴스, 트위터, 유튜브 API를 활용해 뉴스 토픽에서 자주 언급된 키워드와 관련된 데이터를 수집 및 정보 추출

## Getting Started
### Requirements

* OS : Windows 10
* language : python3.8
  * pymysql
  * sqlalchemy
  * eunjeon
  * requests
  * BeautifulSoup
  * tweepy
  * google-api-python-client

## Usage
1. Project Download
2. MySQL DB 생성


![데이터베이스 drawio](https://user-images.githubusercontent.com/89976847/156385448-d710c163-a232-43b5-a8bc-d0f2c33ec63b.png)

3. DB연결

```
engine = create_engine('{DBMS}+pymysql://{USER NAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')
```

4. collect.py 파일 실행: 매일 23:30에 데이터수집 동작

```
schedule.every().day.at("23:30").do(collector)

while True:
    schedule.run_pending()
    time.sleep(1)
```


**topic_trend_keyword by NNN lab.**
