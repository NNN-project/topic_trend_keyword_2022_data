import tweepy
import pandas as pd
import time

# Consumer keys and access tokens, used for OAuth
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

def twitter_search(search_keyword, date):

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    result = []  # 크롤링 텍스트를 저장 할 리스트 변수
    for keyword in search_keyword:
        print(keyword[1])
        time.sleep(10)
        tweets = tweepy.Cursor(api.search_tweets, q=keyword[1], until=date, lang="ko").items(100)
        for tweet in tweets:
            # 해시태그 수집
            hashtag_text = ''
            hashtag = tweet.entities['hashtags']
            if len(hashtag) != 0:
                for i in range(len(hashtag)):
                    hashtag_text += hashtag[i]['text'] + ', '
                hashtag_text = hashtag_text[:-2]
            else:
                hashtag_text = 'empty'
            result.append([tweet.text, tweet.favorite_count, tweet.retweet_count, hashtag_text, tweet.created_at, tweet.id_str, keyword[0]])
    #result = sorted(result, key=lambda x : -x[4]) # 좋아요 수 기준으로 정렬
    #result = sorted(result, reverse=False )

    df = pd.DataFrame(result, columns = ['content', 'like_count', 'retweet', 'tags', 'published', 'writer', 'keyword_id'])
    
    return df
    # print(len(result))  # 크롤링하여 가져온 트윗 개수
    # print(df)  # 크롤링 결과 확인
    # df.to_csv('result.csv', encoding='utf-8-sig')

    # 판다스 time 키의 값 기준으로 쿼리
    # filter_data = df.query("time >= '2022-02-20 00:00:00'")
    # print(filter_data)

    # 수집한 데이터 확인 차 출력
    # for index, row in filter_data.iterrows():
    #     print(row)
    #     print('='*10)