import os
import requests
import boto3
import json
import io
from datetime import datetime

NEWSAPI_KEY = os.environ['NEWSAPI_KEY']
SOURCES = {
    "left": ["cnn"],
    "right": ["fox-news"]
}

# hit the news api
def getNews(sources):
    """
    Get a news feed as json from newsapi.org

    Args:
        sources (list): List of news source strings specified in newsapi.org
    """
    sources = ",".join(sources)
    r = requests.get('https://newsapi.org/v2/top-headlines?apiKey=%s&sources=%s' % (NEWSAPI_KEY, sources))
    return r

def uploadToS3(dict_to_upload):
    """
    Args: 
        dict_to_upload (Dictionary):    Dictionary to convert to json and upload as news.json
    """
    s3 = boto3.client('s3')
    file_buffer = io.BytesIO(bytearray(json.dumps(dict_to_upload), "utf-8"))
    s3.upload_fileobj(file_buffer, 'news', 'polarination.json', \
        ExtraArgs={'ContentType': 'text/json'})

def main():
    left = getNews(SOURCES['left'])
    right = getNews(SOURCES['right'])

    if left.status_code == 200 and right.status_code == 200:
        news_json = {
            'date_created': str(datetime.now()),
            'left': left.json(),
            'right': right.json()
        }

        # send to s3
        uploadToS3(news_json)

def lambda_handler(event, context):
    main()

    return {
        "message": "news updated at %s" % str(datetime.now())
    }