import json
import requests
from pymongo import MongoClient
import os

def send_slack_alert(message):
    webhook_url = os.environ['SLACK_WEBHOOK_URL']
    payload = { "text": message }
    requests.post(webhook_url, json=payload)

def lambda_handler(event, context):
    try:
        message = json.dumps(event, indent=2)
        send_slack_alert(f"🚨 Honeytoken used! Event:\n```{message}```")
        mongo_uri = os.environ['MONGO_URI']
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
        db = client['honeydb']
        db.alerts.insert_one({"event": event})
        return {"status": "Alert sent and logged"}
    except Exception as e:
        return {"error": str(e)}
