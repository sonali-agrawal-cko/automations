import os
import requests
import json

PD_API_KEY = os.getenv('PD_API_KEY')
PD_SCHEDULE_ID = os.getenv('PD_SCHEDULE_ID')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

headers = {
    'Authorization': f'Token token={PD_API_KEY}',
    'Accept': 'application/vnd.pagerduty+json;version=2'
}

params = {
    'schedule_ids[]': PD_SCHEDULE_ID,
    'time_zone': 'UTC'
}

# Get current on-calls for the schedule
response = requests.get('https://api.pagerduty.com/oncalls', headers=headers, params=params)
response.raise_for_status()

oncalls = response.json().get('oncalls', [])

# Debug logging
print(f"Raw response: {json.dumps(response.json(), indent=2)}")
print(f"Number of oncalls found: {len(oncalls)}")
print(f"Schedule ID we're looking for: {PD_SCHEDULE_ID}")

# Filter oncalls by exact schedule ID (double-safety)
filtered_oncalls = [
    o for o in oncalls
    if o.get('schedule') and o['schedule'].get('id') == PD_SCHEDULE_ID
]

print(f"Number of filtered oncalls: {len(filtered_oncalls)}")
if filtered_oncalls:
    print(f"First filtered oncall: {json.dumps(filtered_oncalls[0], indent=2)}")

# Collect user names
user_names = ', '.join(set(o['user']['summary'] for o in filtered_oncalls)) or "No one found 🫠"

# Prepare Slack message
slack_message = {
    "text": f"📆 *Weekly On-Call Update*\nSchedule: *Payment Routing - Incoming Primary*\n👨‍🚒 On Call This Week: {user_names}"
}

# Send to Slack
slack_response = requests.post(SLACK_WEBHOOK_URL, json=slack_message)
slack_response.raise_for_status()

print("✅ Posted on-call update to Slack.")