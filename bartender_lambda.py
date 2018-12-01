import json
import os
import logging
#import urllib
from botocore.vendored import requests

# Grab the Bot OAuth token from the environment.
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Define the URL of the targeted Slack API resource.
# We'll send our replies there.
SLACK_URL = "https://slack.com/api/chat.postMessage"
SLACK_WEBHOOK = "https://hooks.slack.com/services/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"
SLACK_DEL = "https://slack.com/api/chat.delete"

def _getusername(userid):
    payload = {'token': BOT_TOKEN, 'user': userid}
    r = requests.get('https://slack.com/api/users.info', params=payload)
    if r.json()["user"]["real_name"]!='':
        return r.json()["user"]["real_name"]
    elif r.json()["user"]["profile"]["display_name"]!='':
        return r.json()["user"]["profile"]["display_name"]
    else:
        return r.json()["user"]["name"]

def placeorder(drink,userid,username,channelid):
    response = username+" would like a"+drink+". Please let them know when it is ready!"

    data = {"channel": "#bartenders",
            "text":response,
            #"attachments":[{
            #            "fallback": "Unfortunately, the order could not be placed. Please see a bartender.",
            #            "callback_id": "barkeep",
            #            "color": "#3AA3E3",
            #            "attachment_type": "default",
            #            "actions": [
            #             {
            #                 "name": "order|"+username+"|"+channelid,
            #                 "text": "Acknowledge",
            #                 "type": "button",
            #                 "value": "okay"
            #            },
            #            {
            #                "name": "order|"+username+"|"+channelid,
            #                "text": "Deny",
            #                "style": "danger",
            #                "type": "button",
            #                "value": "nope",
            #                "confirm": {
            #                    "title": "Are you sure?",
            #                    "text": "This will delete the user's order.",
            #                    "ok_text": "Yes",
            #                    "dismiss_text": "No"
            #                }
            #            },
            #            {
            #                "name": "order|"+username+"|"+channelid,
            #                "text": "Drink is Ready",
            #                "type": "button",
            #                "value": "ready"
            #            }]
            #        }]
            }
    headers = {
        'Content-Type': 'application/json',
        'Authorizaton': 'Bearer '+BOT_TOKEN
    }
    r=requests.post(SLACK_WEBHOOK,data=json.dumps(data),headers=headers)
    #os.system("curl -X POST -H 'Content-type: application/json' --data "+str(data)+" https://hooks.slack.com/services/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")
    
def lambda_handler(data, context):
    headers = {
        'Content-Type': 'application/json',
        'Authorizaton': 'Bearer '+BOT_TOKEN
    }
    if "challenge" in data:
        return data["challenge"]
    logging.info(str(data))
    slack_event = data['event']
    if "bot_id" in slack_event:
        logging.warn("Ignore bot event")
        logging.warn(str(data))
        #ndata={"text":str(data)}
        #r=requests.post(SLACK_WEBHOOK,data=json.dumps(ndata),headers=headers)
    else:
        if True:
            ndata={"text":str(data)}
            #r=requests.post(SLACK_WEBHOOK,data=json.dumps(ndata),headers=headers)
            
        if "payload" in data:
            #r=requests.post(SLACK_WEBHOOK,data=json.dumps({"text":str(data)}),headers=headers)
            if data["payload"]["actions"][0].get("value")=="nope":
                msg = data["payload"]["message_ts"]
                cid = data["payload"]["channel"]["id"]
                r=requests.post(SLACK_WEBHOOK,data=json.dumps({"text":"deleting"}),headers=headers)
                r=requests.post(SLACK_DEL,data=json.dumps({"ts":msg,"channel":cid}),headers=headers)
                r=requests.post(SLACK_WEBHOOK,data=json.dumps({"text":str(r.json())}),headers=headers)
        else:    
        # Get the text of the message the user sent to the bot,
        # and reverse it.
            text = slack_event["text"]
            if "help" in text or "Help" in text:
                response_text="Can I get you something to drink? Simply type !order [drink name], or consult one of the human bartenders."
            elif "thanks" in text or "Thanks" in text or "Thank you" in text or "thank you" in text:
                response_text="My pleasure!"
            elif "tip" in text or "Tip" in text:
                response_text="I don't accept tips, but your human bartenders might!"
            elif "I'll have a" in text:
                drink = text.split("I'll have a")[1]
                userid=slack_event["user"]
                username=requests.get('https://slack.com/api/users.info', params={"token":BOT_TOKEN,"user":slack_event["user"]}).json()["user"]["real_name"]
                channelid=slack_event["channel"]
                if drink[-1]=="." or drink[-1]=="!" or drink[-1]=="?":
                    drink = drink[:-1]
                placeorder(drink,userid,username,channelid)
                response_text="I'll place an order for "+username+" for a"+drink+"."
            elif "Can I have a" in text:
                drink = text.split("Can I have a")[1]
                userid=slack_event["user"]
                username=requests.get('https://slack.com/api/users.info', params={"token":BOT_TOKEN,"user":slack_event["user"]}).json()["user"]["real_name"]
                channelid=slack_event["channel"]
                if drink[-1]=="." or drink[-1]=="!" or drink[-1]=="?":
                    drink = drink[:-1]
                placeorder(drink,userid,username,channelid)
                response_text="I'll place an order for "+username+" for a"+drink+"."
            elif "I'll order a" in text:
                drink = text.split("I'll order a")[1]
                userid=slack_event["user"]
                username=requests.get('https://slack.com/api/users.info', params={"token":BOT_TOKEN,"user":slack_event["user"]}).json()["user"]["real_name"]
                channelid=slack_event["channel"]
                if drink[-1]=="." or drink[-1]=="!" or drink[-1]=="?":
                    drink = drink[:-1]
                placeorder(drink,userid,username,channelid)
                response_text="I'll place an order for "+username+" for a"+drink+"."
            elif "I'll have an" in text:
                drink = text.split("I'll have a")[1]
                userid=slack_event["user"]
                username=requests.get('https://slack.com/api/users.info', params={"token":BOT_TOKEN,"user":slack_event["user"]}).json()["user"]["real_name"]
                channelid=slack_event["channel"]
                if drink[-1]=="." or drink[-1]=="!" or drink[-1]=="?":
                    drink = drink[:-1]
                placeorder(drink,userid,username,channelid)
                response_text="I'll place an order for "+username+" for a"+drink+"."
            elif "Can I have an" in text:
                drink = text.split("Can I have a")[1]
                userid=slack_event["user"]
                username=requests.get('https://slack.com/api/users.info', params={"token":BOT_TOKEN,"user":slack_event["user"]}).json()["user"]["real_name"]
                channelid=slack_event["channel"]
                if drink[-1]=="." or drink[-1]=="!" or drink[-1]=="?":
                    drink = drink[:-1]
                placeorder(drink,userid,username,channelid)
                response_text="I'll place an order for "+username+" for a"+drink+"."
            elif "Can I get a" in text:
                drink = text.split("Can I get a")[1]
                userid=slack_event["user"]
                username=requests.get('https://slack.com/api/users.info', params={"token":BOT_TOKEN,"user":slack_event["user"]}).json()["user"]["real_name"]
                channelid=slack_event["channel"]
                if drink[-1]=="." or drink[-1]=="!" or drink[-1]=="?":
                    drink = drink[:-1]
                placeorder(drink,userid,username,channelid)
                response_text="I'll place an order for "+username+" for a"+drink+"."
            elif "Can I get an" in text:
                drink = text.split("Can I get a")[1]
                userid=slack_event["user"]
                username=requests.get('https://slack.com/api/users.info', params={"token":BOT_TOKEN,"user":slack_event["user"]}).json()["user"]["real_name"]
                channelid=slack_event["channel"]
                if drink[-1]=="." or drink[-1]=="!" or drink[-1]=="?":
                    drink = drink[:-1]
                placeorder(drink,userid,username,channelid)
                response_text="I'll place an order for "+username+" for a"+drink+"."
                
            elif "I'll order an" in text:
                drink = text.split("I'll order a")[1]
                userid=slack_event["user"]
                username=requests.get('https://slack.com/api/users.info', params={"token":BOT_TOKEN,"user":slack_event["user"]}).json()["user"]["real_name"]
                channelid=slack_event["channel"]
                if drink[-1]=="." or drink[-1]=="!" or drink[-1]=="?":
                    drink = drink[:-1]
                placeorder(drink,userid,username,channelid)
                response_text="I'll place an order for "+username+" for a"+drink+"."
                
            elif "!order" in text:
                drink = text.split("!order")[1]
                userid=slack_event["user"]
                username=requests.get('https://slack.com/api/users.info', params={"token":BOT_TOKEN,"user":slack_event["user"]}).json()["user"]["real_name"]
                channelid=slack_event["channel"]
                if drink[-1]=="." or drink[-1]=="!" or drink[-1]=="?":
                    drink = drink[:-1]
                placeorder(drink,userid,username,channelid)
                response_text="I'll place an order for "+username+" for a"+drink+"."
            elif "hello" in text or "Hello" in text or "hey" in text or "Hey" in text or "hi" in text or "Hi" in text:
                response_text="Hi there! Can I get you something to drink? Simply type !order [drink name], or consult one of the human bartenders."
            else:
                response_text="I'm not sure how to help with that. Try ordering a drink with !order [drink name], or consult one of the human bartenders."
        
        # Get the ID of the channel where the message was posted.
            channel_id = slack_event["channel"]
        
        # We need to send back three pieces of information:
        #     1. The reversed text (text)
        #     2. The channel id of the private, direct chat (channel)
        #     3. The OAuth token required to communicate with 
        #        the API (token)
        # Then, create an associative array and URL-encode it, 
        # since the Slack API doesn't not handle JSON (bummer).
            #data = urllib.parse.urlencode(
            #    (
            #        ("token", BOT_TOKEN),
            #        ("channel", channel_id),
            #        ("text", response_text)
            #    )
            #)
            #data = data.encode("ascii")
            data = {"token":BOT_TOKEN,"channel":channel_id,"text":response_text}
        # Construct the HTTP request that will be sent to the Slack API.
        #request = urllib.request.Request(
        #    SLACK_URL, 
        #    data=data, 
        #    method="POST"
        #)
        # Add a header mentioning that the text is URL-encoded.
        #request.add_header(
        #    "Content-Type", 
        #    "application/x-www-form-urlencoded"
        #)
        
        # Fire off the request!
        #urllib.request.urlopen(request).read()
        r=requests.post(SLACK_URL,data)
        return "I think this worked?"
    return "200 OK"
