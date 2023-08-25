import os
import requests
import time
import json
from wag_advanced_analytics_utils.logger import Logger


class Metrics:
    prefix = "unknown_application"
    if "METRICS_PREFIX" in os.environ:
        prefix = os.environ["METRICS_PREFIX"]
    elif "WAG_SYSTEM" in os.environ:
        prefix = f'wag.{os.environ["WAG_SYSTEM"]}.'

    Logger.debug(f'Using: "{prefix}" as prefix for keys.')
    Logger.debug(
        f'Metrics env: {os.environ["ENVIRONMENT"]}. AWS execution env: {os.environ["AWS_EXECUTION_ENV"]}'
    )

    @staticmethod
    def __format_tags_for_api_request(tags):
        items = tags.items()
        result = []

        for item in items:
            tag = item[0]
            value = item[1]

            result.append(f"{tag}:{value}")

        return result

    @classmethod
    def increment(cls, metric, tags=None, value=1, metric_type="rate"):
        if os.environ["ENVIRONMENT"] != "production":
            return

        actual_value = value
        interval = 10

        if metric_type == "rate":
            actual_value = value / interval

        formatted_tags = []
        if tags != None:
            formatted_tags = cls.__format_tags_for_api_request(tags)

        date_in_seconds = int(round(time.time()))
        payload = {
            "series": [
                {
                    "metric": f"{cls.prefix}{metric}",
                    "points": [[date_in_seconds, actual_value]],
                    "type": metric_type,
                    "interval": interval,
                    "tags": [*formatted_tags, "request:api"],
                },
            ]
        }

        try:
            Logger.debug("Reporting metric.", payload)
            response = requests.post(
                f'https://api.datadoghq.com/api/v1/series?api_key={os.environ["DATADOG_API_KEY"]}&app_key={os.environ["DATADOG_APP_KEY"]}',
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
            )
            Logger.debug("Datadog response", {"response": response.json()})
        except Exception as error:
            Logger.error(
                f"Could not POST metric to Datadog. Error: [{str(error)}]",
                {"metric": metric, "payload": payload},
            )
