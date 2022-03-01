from apiclient.discovery import build
import pandas as pd

# API KEY
DEVELOPER_KEY = ""

# SERVICE, VERSION
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# CATEGORIES
CATEGORIES_DICT = {
    "1": "Film & Animation", "2": "Autos & Vehicles",
    "10": "Music", "15": "Pets & Animals",
    "17": "Sports", "18": "Short Movies",
    "19": "Travel & Events", "20": "Gaming",
    "21": "Videoblogging", "22": "People & Blogs",
    "23": "Comedy", "24": "Entertainment",
    "25": "News & Politics", "26": "Howto & Style",
    "27": "Education", "28": "Science & Technology",
    "30": "Movies", "31": "Anime/Animation",
    "32": "Action/Adventure", "33": "Classics",
    "34": "Comedy", "35": "Documentary",
    "36": "Drama", "37": "Family",
    "38": "Foreign", "39": "Horror",
    "40": "Sci-Fi/Fantasy", "41": "Thriller",
    "42": "Shorts", "43": "Shows",
    "44": "Trailers",
}

# INPUT = List(str...), Int(Maximum Number Of Results), Int(yymmdd)
# OUTPUT = File(.csv)..., Str
def youtube_search(search_keyword, date):
    # 매개변수 설정
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)
    # 결과 리스트
    publishedAt = []
    title = []
    tags = []
    channel = []
    category = []
    viewCount = []
    likeCount = []
    commentCount = []
    keyword_id = []
    # keyword에 따른 검색
    for keyword in search_keyword:
        search_response = youtube.search().list(
            q=keyword[1],
            part="id,snippet",
            regionCode="KR",
            publishedAfter=date,
            maxResults=20
        ).execute()
        # 리스트에 담기
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                # + Primary Key => yt_220219_keyword?
                # + Keyword Column
                # videoId.append(search_result["id"]["videoId"])
                # 2022-02-19T10:25:44Z => 2022-02-19?
                publishedAt.append(search_result["snippet"]["publishedAt"].split('T')[0])
                channel.append(search_result["snippet"]["channelTitle"])
                # video ID에 따른 검색
                counts = youtube.videos().list(
                    id=search_result["id"]["videoId"],
                    part="snippet,statistics"
                ).execute()
                counts = counts.get("items", [])
                title.append(counts[0]["snippet"]["title"])
                # How many tags should I include? 
                # which Format? Array or String or Columns
                try:
                    tag = counts[0]["snippet"]["tags"]
                    tags.append(', '.join(tag))
                except KeyError:
                    tags.append('empty')
                try:
                    category.append(CATEGORIES_DICT[counts[0]["snippet"]["categoryId"]])
                except KeyError:
                    category.append('empty')
                viewCount.append(counts[0]["statistics"]["viewCount"])
                try:
                    likeCount.append(counts[0]["statistics"]["likeCount"])
                except KeyError:
                  likeCount.append("0")
                try:
                    commentCount.append(counts[0]["statistics"]["commentCount"])
                except KeyError:
                    commentCount.append("0")
                keyword_id.append(keyword[0])
    # 데이터 프레임
    df = pd.DataFrame({
        "title" : title, "published" : publishedAt, 
        "tags" : tags, "channel_name" : channel,
        "category" : category, "view_count" : viewCount, 
        "like_count" : likeCount, "comment_count" : commentCount,
        "keyword_id" : keyword_id
        })
    # 저장
    # df.to_csv(f"{date}_youtube_{keyword}.csv", index=False, encoding="utf-8")
    return df

