import datetime
import boto3
import requests
import urllib
import pytz
import os
import time

AWS_REGION = os.environ['AWS_REGION']
AWS_KEY_ID = os.environ['AWS_KEY_ID']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']


if __name__ == '__main__':
    while True:
        client = boto3.client(
            'cloudwatch',
            aws_access_key_id=AWS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION,
        )

        end = datetime.datetime.now()
        start = datetime.datetime(end.year, end.month, 1)
        response = client.get_metric_statistics (
            MetricName = 'EstimatedCharges',
            Namespace  = 'AWS/Billing',
            Period     = 60*60*24*7,
            StartTime  = start,
            EndTime    = end,
            Statistics = ['Maximum'],
            Dimensions = [
                {
                    'Name': 'Currency',
                    'Value': 'USD'
                }
            ]
        )

        text = ''
        for resp in response['Datapoints']:
            maximum = resp['Maximum']
            date    = resp['Timestamp'].strftime('%Y年%m月%d日')
            text += "%sから%sまでのAWSの料金は、$%sです。\n" % (start.strftime('%Y年%m月%d日'), date, maximum)

        params = {'token': SLACK_TOKEN,   # トークン
                 'channel': SLACK_CHANNEL, # チャンネルID
                 'text': text    # 送信するテキスト
        }

        params = urllib.parse.urlencode(params)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        requests.get("https://slack.com/api/chat.postMessage", params=params, headers=headers)
        time.sleep(60*60*24)
