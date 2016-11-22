import datetime
import boto.ec2.cloudwatch
import env
import requests
import urllib

conn = boto.ec2.cloudwatch.connect_to_region(
    AWS_REGION,
    aws_access_key_id=env.AWS_KEY_ID,
    aws_secret_access_key=env.AWS_SECRET_KEY)

end = datetime.datetime.utcnow()
start = datetime.datetime(end.year, end.month, 1)
　
services = conn.list_metrics()

text = ''

for service in services:
    value = conn.get_metric_statistics(
        3600,
        start,
        end,
        'EstimatedCharges',
        'AWS/Billing',
        'Maximum',
        dimensions = {'ServiceName':[service], 'Currency':['USD']}

        if not value:
                continue
        text += service + ': '
        text += str(value) + '/'
        text +=  str(value[0]['Maximum']) + '\n'

params = {'token':env.SLACK_TOKEN,   # トークン
         'channel':'admin', # チャンネルID
         'text': 'bot'    # 送信するテキスト
}
params = urllib.parse.urlencode(params)
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
requests.get("https://slack.com/api/chat.postMessage", params=params, headers=headers)
