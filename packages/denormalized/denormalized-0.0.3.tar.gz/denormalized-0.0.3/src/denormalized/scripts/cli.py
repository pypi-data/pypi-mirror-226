import json
from types import SimpleNamespace
from typing import Annotated

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from denormalized import DenormalizedClient

console = Console()

app = typer.Typer()


def _process_json_str(string: str):
    """Strip leading/trailing newlines, qauotes, and slashes from json strings passed in"""
    return string.replace("\\n", "").replace("\\", "").strip("\"'")


@app.callback()
def main(
    ctx: typer.Context,
    auth_token: Annotated[
        str,
        typer.Option(
            envvar=[
                "PROPELAUTH_TOKEN",
                "LOCAL_PROPELAUTH_TOKEN",
            ]
        ),
    ],
    url: Annotated[
        str, typer.Option(envvar="DENORMALIZED_URL")
    ] = "http://localhost:3001/v1",
):
    ctx.obj = SimpleNamespace(client=DenormalizedClient(api_key=auth_token, url=url))


@app.command()
def create_topic(
    ctx: typer.Context,
    name: Annotated[str, typer.Option()],
    key: Annotated[str, typer.Option()],
    events: Annotated[str, typer.Option()],
):
    try:
        _events = json.loads(_process_json_str(events))
    except Exception as e:
        print("Unable to de-serialize event data", e)
        raise typer.Exit(-1)

    if isinstance(_events, dict):
        _events = [_events]

    if len(_events) == 0:
        print("Please pass some _events")
        raise typer.Exit(-1)

    if not _events[0].get(key):
        print(f"sample event does not contain key: {key} property")
        raise typer.Exit(-1)

    try:
        res = ctx.obj.client.create_topic(name, key, _events)
        print("topic created")
        print(res)
    except Exception as e:
        print("Failed to create topic", e)


@app.command()
def query(
    ctx: typer.Context,
    sql: Annotated[str, typer.Argument()],
):
    res = ctx.obj.client.query(sql)
    table = Table(
        *res["resultTable"]["dataSchema"]["columnNames"],
    )
    for row in res["resultTable"]["rows"]:
        table.add_row(*[str(c) for c in row])

    console.print(table)


@app.command("topics")
def list_topics(ctx: typer.Context):
    topics = ctx.obj.client.get_topics()
    print(topics)


@app.command("delete")
def delete_topics(
    ctx: typer.Context,
    topic_name: Annotated[str, typer.Argument()],
):
    try:
        ctx.obj.client.delete_topic(topic_name)
        print(f"{topic_name} successfully deleted")
    except Exception as e:
        print(f"Error deleting {topic_name}: {e}")


@app.command("emit")
def produce_events(
    ctx: typer.Context,
    topic_name: Annotated[str, typer.Argument()],
    events: Annotated[str, typer.Argument()],
):
    try:
        _events = json.loads(_process_json_str(events))
    except Exception as e:
        print("Unable to de-serialize event data", e)
        raise typer.Exit(-1)

    try:
        ctx.obj.client.produce_events(topic_name, _events)
        print(f"{len(_events)} successfully emitted")
    except Exception as e:
        print(f"Error emitting events: {e}")


if __name__ == "__main__":
    app()
