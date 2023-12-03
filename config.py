import os

config = {
    # general
    "slackbot_port": int(os.environ.get("WIREBOT_SLACKBOT_PORT", "3000")),
    "slack_bot_token": os.environ["WIREBOT_BOT_TOKEN"],
    "slack_signing_secret": os.environ["WIREBOT_SIGNING_SECRET"],

    # statuscake
    "statuscake_api_key": os.environ.get("WIREBOT_STATUSCAKE_API_KEY"),
    "statuscake_check_id": "7013710",
    "statuscake_port": int(os.environ.get("WIREBOT_WEBHOOK_PORT", "5000")),
    "statuscake_debug": bool(os.environ.get("WIREBOT_WEHOOK_DEBUG")),
    "statuscake_notif_channel_id": "C05V41TAERK",

    # github
    "github_port": int(os.environ.get("WIREBOT_WEBHOOK_PORT", "5001")),
    "github_notif_channel_id": "C05V41TAERK",
    "github_access_token": os.environ["WIREBOT_GITHUB_ACCESS_TOKEN"],
    "github_repo": "ajmalsiddiqui/ajmals-website",

    # Google Analytics
    "ga_property_id": os.environ["WIREBOT_GOOGLE_ANALYTICS_PROPERTY_ID"],
}
