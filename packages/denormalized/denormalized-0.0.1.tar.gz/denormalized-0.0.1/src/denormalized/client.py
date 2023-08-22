from typing import Any

import httpx

DEFAULT_API_URL = "https://api.denormalized.io/v1"


class TopicCreateError(Exception):
    pass


class TopicDeleteError(Exception):
    pass


class QueryError(Exception):
    pass


class ProduceEventError(Exception):
    pass


Event = dict[str, Any]


class DenormalizedClient:
    def __init__(
        self,
        api_key: str,
        url: str = DEFAULT_API_URL,
    ):
        self._client = httpx.Client(
            base_url=url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )

    def get_topics(self) -> list[dict]:
        res = self._client.get("/topics/")
        topics = res.json()
        return topics["topics"]

    def create_topic(self, topic_name: str, event_key: str, events: list[dict]) -> None:
        res = self._client.post(
            "/topics/",
            json={
                "topic_name": topic_name,
                "event_key": event_key,
                "events": events,
            },
        )

        if res.status_code != 200:
            raise TopicCreateError(res.json())

        data = res.json()
        return data["topic"]

    def delete_topic(self, topic_name: str) -> None:
        res = self._client.delete(f"/topics/{topic_name}")

        if res.status_code != 200:
            raise TopicDeleteError(res.json())

    def produce_events(self, topic_name: str, events: list[Event] | Event) -> None:
        if not isinstance(events, list):
            events = [events]

        res = self._client.post(f"/topics/{topic_name}", json=events)

        if res.status_code != 200:
            raise ProduceEventError(res.json())

    def query(self, sql):
        res = self._client.post("/query/", json={"sql": sql})

        if res.status_code != 200:
            raise QueryError(res.json())

        return res.json()["result"]
