# core/notion_push.py

from notion_client import Client
import os

token = os.getenv("QB_NOTION_TOKEN")
page_id = os.getenv("QB_NOTION_PAGE")
client = Client(auth=token)

def push(markdown: str, title="Creative Brief"):
    blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": line}}
                ]
            },
        }
        for line in markdown.splitlines()
    ]

    client.pages.create(
        parent={"page_id": page_id},
        properties={"title": [{"text": {"content": title}}]},
        children=blocks,
    )

