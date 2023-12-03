from flask import request
from github import Github

from plugin import Plugin
from webhook_server import WebhookServer

class GithubPlugin(Plugin):
    def __init__(self, slack_client, webhook_port, github_repo, github_client, slack_notif_channel_id):
        super().__init__("github", slack_client)
        self.webhook_port = webhook_port
        self.github_client = github_client
        self.github_repo = self.github_client.get_repo(github_repo)
        self.slack_notif_channel_id = slack_notif_channel_id

    def setup(self, debug=False):
        def handler():
            data = request.json
            message = f"{data['pusher']['name']} pushed to {data['ref']}"
            self.slack_client.chat_postMessage(
                channel=self.slack_notif_channel_id,
                text=message,
            )
            return "ok"

        self.webhook_server = WebhookServer(
            f"{self.name}_webhook_server",
            self.webhook_port,
            handler,
            debug,
        )

        self.webhook_server.start()

    def teardown(self):
        self.webhook_server.teardown()

    def handle_mention(self, event, slack_client):
        text = event.get("text")
        if "github" in text:
            pushes = list(self.github_repo.get_commits()[:5])
            message = "Last 5 pushes:\n"
            for i, push in enumerate(pushes):
                message += f"{i}. '{push.commit.message}' by {push.committer.name} at {push.commit.committer.date}\n"


            channel_id = event.get("channel")

            self.slack_client.chat_postMessage(
                channel=channel_id,
                text=message,
            )
