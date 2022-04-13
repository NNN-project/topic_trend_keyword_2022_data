# 스케줄러
import schedule
import time

# 라이브러리
from datetime import date
import pandas as pd

# 네이버, 유튜브, 트위터, 키워드
from naver import naver_news
from youtube import youtube_search
from twitter import twitter_search

# 데이터베이스
import pymysql
from sqlalchemy import create_engine

# 키워드 추출
from eunjeon import Mecab
from collections import Counter

def news_keyword(data, date):
    m = Mecab()
    keywords = []
    stopword = ['뉴스','뉴스데스크','영상','단독','자막','클로징','종합','헤드라인','특보','김반장','앵커',
                '내일','오늘','하루','시간','오후','전국','아침','곳곳','나흘','개월','날씨','이번','동안','올해','사흘',
            '주말','이틀']
    for i in data['title']:
        title = m.nouns(i)
        for j in title:
            if len(j) > 1 and j not in stopword:
                keywords.append(j)
            if j == '두기' and keywords[-2] == '거리':
                del keywords[-2:]
                keywords.append('거리두기')
    #데이터 카운트
    count = Counter(keywords)
    #데이터 순서대로 데이터프레임 작성
    sort = count.most_common()
    keyword_id = []
    keyword = []
    weight = []
    for word in sort[:50]:
        keyword_id.append(f'{date}_{word[0]}')
        keyword.append(word[0])
        weight.append(word[1])
    df = pd.DataFrame({
        'keyword_id':keyword_id, 'keyword':keyword, 
        'weight':weight, 'c_date':date
    })
    return df

def collector():
    # 엔진 설정
    engine = create_engine('mysql+pymysql://admin:******@tkt-db-ko.cnirlhwrm55r.ap-northeast-2.rds.amazonaws.com:3306/topic_keywords_db')

    # today '2022-02-26', day '22-02-26', day_str '2022-02-26T00:00:00Z'
    today = date.today()
    day = today.strftime("%y-%m-%d")
    day_str = day+"T00:00:00Z"

    # 네이버 뉴스 수집, DB에 저장
    naver = naver_news(today.strftime("%Y-%m-%d"))
    naver.to_sql(name='naverNews', con=engine, index=False, if_exists='append')

    # 키워드 추출, DB에 저장
    data = pd.read_sql_query(f"SELECT * FROM `naverNews` WHERE DATE(c_date) = DATE({today});", engine)
    keyword_data = news_keyword(data, day)
    keyword_data.to_sql(name='keyword', con=engine, index=False, if_exists='append')

    # 상위 10개 키워드, 키워드ID 리스트로 가져오기
    # 22-02-26 회의 : 10위 키워드와 weight값이 동일한 키워드 포함
    weight_df = pd.read_sql_query("SELECT weight FROM `keyword` WHERE DATE(c_date) = DATE(NOW()) ORDER BY weight DESC LIMIT 10;", engine)
    weight_low = weight_df.values.tolist()[-1][0]
    keyword_df = pd.read_sql_query(f"SELECT keyword_id, keyword FROM `keyword` WHERE DATE(c_date) = DATE(NOW()) AND weight >= {weight_low};", engine)
    keyword_list = keyword_df.values.tolist()
    
    # 트위터 데이터 수집 API
    # tweepy.errors.TooManyRequests: 429 Too Many Requests
    # https://developer.twitter.com/en/docs/basics/rate-limiting
    # 슬립 10초 사용 > 100개 성공 // RT 미포함으로 받으려면?
    # 같은 조건에서 다시 실행 > 실패 이유는 모름...
    twitter_data = twitter_search(keyword_list, today)
    twitter_data.to_sql(name='twitter', con=engine, index=False, if_exists='append')
    
    # 유튜브 데이터 수집 API
    # 22-02-26 회의 : 오늘 생성된 리소스만 검색
    youtube_data = youtube_search(keyword_list, day_str)
    youtube_data.to_sql(name='youtube', con=engine, index=False, if_exists='append')
    
    print('Done')


schedule.every().day.at("23:30").do(collector)

while True:
    schedule.run_pending()
    time.sleep(1)
