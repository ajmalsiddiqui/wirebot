import logging
import threading

from slack_bolt import App
from statuscake import ApiClient
from github import Github
from google.analytics.data_v1beta import BetaAnalyticsDataClient

from plugins.hello import HelloPlugin
from plugins.statuscake import StatuscakePlugin, get_client
from plugins.github import GithubPlugin
from plugins.google_analytics import GoogleAnalyticsPlugin
from config import config

app = App(
    token=config["slack_bot_token"],
    signing_secret=config["slack_signing_secret"],
)


plugins = [
    HelloPlugin(slack_client=app.client, message_template="Bonjour, <@{user}>"),
    StatuscakePlugin(
        slack_client=app.client,
        webhook_port=config["statuscake_port"],
        check_id=config["statuscake_check_id"],
        statuscake_client=get_client(config["statuscake_api_key"]),
        slack_notif_channel_id=config["statuscake_notif_channel_id"],
    ),
    GithubPlugin(
        slack_client=app.client,
        webhook_port=config["github_port"],
        github_repo=config["github_repo"],
        github_client=Github(config["github_access_token"]),
        slack_notif_channel_id=config["github_notif_channel_id"],
    ),
    GoogleAnalyticsPlugin(
        slack_client=app.client,
        ga_client=BetaAnalyticsDataClient(),
        property_id=config["ga_property_id"],
    )
]

for plugin in plugins:
    if plugin.enabled:
        print(f"Setting up plugin {plugin.name}")
        plugin.setup()

@app.event("app_mention")
def handle_mention(event, client):
    global plugins

    for plugin in plugins:
        if plugin.enabled:
            plugin.handle_mention(event, client)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    app.start(config["slackbot_port"])
