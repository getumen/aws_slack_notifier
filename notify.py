import datetime
import boto3
import requests
import urllib
import pytz
import os

AWS_REGION = os.environ['AWS_REGION']
AWS_KEY_ID = os.environ['AWS_KEY_ID']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
SLACK_TOKEN = os.environ['SLACK_TOKEN']


if __name__ == '__main__':
    client = boto3.client(
        'cloudwatch',
        aws_access_key_id=AWS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    print(client.describe_alarm_history())

    end = datetime.datetime.utcnow()
    start = datetime.datetime(end.year, end.month, 1)

    text = ''

    params = {'token':SLACK_TOKEN,   # トークン
             'channel':'admin', # チャンネルID
             'text': 'bot'    # 送信するテキスト
    }

    params = urllib.parse.urlencode(params)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#    requests.get("https://slack.com/api/chat.postMessage", params=params, headers=headers)
