# Topic_Trend_Keyword 데이터수집

네이버 뉴스, 트위터, 유튜브 API를 활용해 뉴스 토픽에서 자주 언급된 키워드와 관련된 데이터를 수집 및 정보 추출

## Getting Started
### Dependencies

* 데이터베이스 모듈
  * pymysql
  * sqlalchemy
* 형태소분류 모듈
  * eunjeon
* 네이버 데이터수집 모듈
  * requests
  * BeautifulSoup
* 트위터 API사용을 위한 모듈
  * tweepy
* apiclient.discovery 모듈설치
  * google-api-python-client

## Usage
1. Project Download
2. MySQL DB와 테이블 생성


![데이터베이스 drawio](https://user-images.githubusercontent.com/89976847/156385448-d710c163-a232-43b5-a8bc-d0f2c33ec63b.png)


3. collect.py 파일 실행: 매일 23:30에 데이터수집 동작

```
schedule.every().day.at("23:30").do(collector)

while True:
    schedule.run_pending()
    time.sleep(1)
```

4. 수집한 데이터 DB에서 추출하기
* keyword_query에서 DB정보 입력 후 이용

```
pymysql.connect(host='', port=3306, user='', password='', db='', charset='utf8')
```


**topic_trend_keyword by NNN lab.**
