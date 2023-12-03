import threading

from flask import request
from statuscake import ApiClient
from statuscake.apis import (
    UptimeApi,
)

from plugin import Plugin
from webhook_server import WebhookServer
from util import quickchart, slack_image_block, slack_text_block

class StatuscakePlugin(Plugin):
    def __init__(self, slack_client, webhook_port, check_id, statuscake_client, slack_notif_channel_id):
        super().__init__("statuscake", slack_client)
        self.statuscake_client = statuscake_client
        self.check_id = check_id
        self.webhook_port = webhook_port
        self.slack_notif_channel_id = slack_notif_channel_id

        self.service = UptimeApi(api_client=self.statuscake_client)

    def setup(self, debug=False):
        def handler():
            message = "Alert: your site is down!"
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
        # TODO regex?
        if "uptime" in text:
            channel_id = event.get("channel")

            uptime_test = self.service.get_uptime_test(self.check_id)["data"]
            uptime = float(uptime_test["uptime"])

            chart = quickchart("doughnut", {
                "labels": ["Uptime", "Downtime"],
                "datasets": [{
                    "data": [uptime, 100-uptime],
                }]
            })

            message = (
                f"Uptime report for check {self.check_id} ({uptime_test['name']}):\n"
                f"Status: {uptime_test['status']}\n"
                f"Last Checked At: {uptime_test['last_tested_at']}\n"
                f"Uptime: {uptime_test['uptime']}\n"
            )

            slack_client.chat_postMessage(
                channel=channel_id,
                text=message,
                blocks=[
                    slack_text_block(message),
                    slack_image_block("Uptime History", chart),
                ],
            )

def get_client(api_key):
    return ApiClient(
        header_name='Authorization',
        header_value=f"Bearer {api_key}"
    )
