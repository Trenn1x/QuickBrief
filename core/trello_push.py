# core/trello_push.py
"""
Create a Trello card that contains the given markdown.

Environment variables required
------------------------------
TRELLO_KEY   – API key for your Trello developer account
TRELLO_TOKEN – user token that grants write access
TRELLO_LIST  – ID of the Trello list the card should be created in
"""

from __future__ import annotations

import os
from datetime import datetime

import requests


def push(markdown: str, title: str | None = None) -> str:
    """Push *markdown* to Trello and return the card’s short URL.

    A missing or non-2xx response raises :class:`requests.HTTPError`.
    """
    trello_key   = os.environ["TRELLO_KEY"]
    trello_token = os.environ["TRELLO_TOKEN"]
    trello_list  = os.environ["TRELLO_LIST"]

    # Auto-generate a reasonable card title if none supplied
    if not title:
        for line in markdown.splitlines():
            line = line.strip()
            if line:
                title = line[:100]            # first non-empty line, max 100 chars
                break
        else:
            title = f"QuickBrief {datetime.now():%Y-%m-%d %H:%M:%S}"

    resp = requests.post(
        "https://api.trello.com/1/cards",
        params={
            "idList": trello_list,
            "key": trello_key,
            "token": trello_token,
        },
        data={
            "name": title,
            "desc": markdown,
        },
        timeout=15,
    )

    # Helpful one-liner that shows up in the Streamlit console
    print("Trello status:", resp.status_code, resp.text[:200])

    resp.raise_for_status()          # raises if Trello didn’t return 2xx
    return resp.json()["shortUrl"]

