from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

from plugin import Plugin
from util import quickchart, slack_image_block

class GoogleAnalyticsPlugin(Plugin):
    def __init__(self, slack_client, ga_client, property_id):
        super().__init__("google-analytics", slack_client)
        self.slack_client = slack_client
        self.ga_client = ga_client
        self.property_id = property_id

    def setup(self):
        pass

    def teardown(self):
        pass

    def handle_mention(self, event, slack_client):
        text = event.get("text")
        if "analytics" in text:
            channel_id = event.get("channel")

            data = self._active_users_by_country()

            limit = 5
            other_count = sum(list(data.values())[limit:])

            truncated_data = dict(zip(list(data.keys())[:limit], list(data.values())[:limit]))
            truncated_data["other"] = other_count

            print(truncated_data)

            chart = quickchart("pie", {
                "labels": list(truncated_data.keys()),
                "datasets": [{
                    "data": list(truncated_data.values()),
                }]
            })

            slack_client.chat_postMessage(
                channel=channel_id,
                # text=message,
                blocks=[
                    slack_image_block("User Distribution by Country", chart),
                ],
            )

    def _active_users_by_country(self):
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[Dimension(name="country")],
            # dimensions=[Dimension(name="city")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date="2020-03-31", end_date="today")],
        )

        response = self.ga_client.run_report(request)

        data = {}

        for row in response.rows:
            data[row.dimension_values[0].value.replace(" ", "_")] = int(row.metric_values[0].value)

        return data
