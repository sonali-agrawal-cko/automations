import requests
import os
from datetime import datetime, timedelta

PD_API_KEY = os.getenv('PD_API_KEY')
SCHEDULE_ID = os.getenv('PD_SCHEDULE_ID')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

today = datetime.utcnow()
monday = today - timedelta(days=today.weekday())
sunday = monday + timedelta(days=6)
since = monday.strftime('%Y-%m-%dT00:00:00Z')
until = sunday.strftime('%Y-%m-%dT23:59:59Z')

headers = {
    'Authorization': f'Token token={PD_API_KEY}',
    'Accept': 'application/vnd.pagerduty+json;version=2'
}
params = {'since': since, 'until': until}
url = f'https://api.pagerduty.com/schedules/{SCHEDULE_ID}/users'

response = requests.get(url, headers=headers, params=params)
users = response.json().get('users', [])
user_names = ', '.join([u['summary'] for u in users]) or "No one found 🫠"

slack_msg = {
    "text": f"📆 *Weekly On-Call Update*\nSchedule: *Payment Routing - Incoming Primary*\n👨‍🚒 On Call This Week: {user_names}"
}
requests.post(SLACK_WEBHOOK_URL, json=slack_msg)
