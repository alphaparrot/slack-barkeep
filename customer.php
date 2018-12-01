<?php

/*

REQUIREMENTS

* A custom slash command on a Slack team
* A web server running PHP5 with cURL enabled

USAGE

* Place this script on a server running PHP5 with cURL.
* Set up a new custom slash command on your Slack team: 
  http://my.slack.com/services/new/slash-commands
* Under "Choose a command", enter whatever you want for 
  the command. /isitup is easy to remember.
* Under "URL", enter the URL for the script on your server.
* Leave "Method" set to "Post".
* Decide whether you want this command to show in the 
  autocomplete list for slash commands.
* If you do, enter a short description and usage hint.

*/

#Got it!
header('X-PHP-Response-Code: 200', true, 200);

# Grab some of the values from the slash command, create vars for post back to Slack
#$command = $_POST['command'];
$text = $_POST['text'];
$username = $_POST['user_name'];
$userid = $_POST["user_id"];
$channel_id = $_POST["channel_id"];
$response_url = $_POST["response_url"];

function slack($message, $channel, $userid, $username, $channel_id, $response_url)
{
    $ch = curl_init("https://slack.com/api/chat.postMessage");
    $data = http_build_query([
        "token" => "YEf22XTCjLOu3YEuuZ7BDRAm",
    	"channel" => $channel, //"#mychannel",
    	"text" => $message, //"Hello, Foo-Bar channel message.",
    	"username" => "Barkeep",
    	"attachments": [
        {
            "fallback": "You are unable to order a drink",
            "callback_id": "barkeep",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "order",
                    "text": "Acknowledge",
                    "type": "button",
                    "value": "okay"
                },
                {
                    "name": "order",
                    "text": "Deny",
                    "style": "danger",
                    "type": "button",
                    "value": "nope",
                    "confirm": {
                        "title": "Are you sure?",
                        "text": "This will delete the user's order.",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
                },
                {
                    "name": "order",
                    "text": "Drink is Ready",
                    "type": "button",
                    "value": "ready"
                }
            ]
        }
    ]
    ]);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $result = curl_exec($ch);
    curl_close($ch);
    
    return $result;
}


slack($username+" would like a "+$text+".","#bartender",$userid,$username,$channel_id,$response_url);

echo "Thanks; order submitted!";

