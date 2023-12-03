from abc import ABC, abstractmethod

class Plugin(ABC):
    def __init__(self, name, slack_client, enabled=True):
        self.name = name
        self.slack_client = slack_client
        self.enabled = enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    @abstractmethod
    def setup(self, *args, **kwargs):
        pass

    @abstractmethod
    def teardown(self, *args, **kwargs):
        pass

    @abstractmethod
    def handle_mention(self, event, client):
        pass

    def __repr__(self):
        return f"{self.name} ({'enabled' if self.enabled else 'disabled'})"

    def __str__(self):
        return f"Plugin<{self.name}>"
