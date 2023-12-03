from plugin import Plugin

class HelloPlugin(Plugin):
    def __init__(self, slack_client, message_template="Hello, <@{user}>"):
        super().__init__("hello", slack_client)
        self.message_template = message_template
        
    def setup(self):
        pass

    def teardown(self):
        pass

    def handle_mention(self, event, client):
        channel_id = event.get("channel")
        text = event.get("text")

        if text and "hello" in text.lower():
            client.chat_postMessage(
                channel=channel_id,
                text=self.message_template.format(user=event['user']),
            )
