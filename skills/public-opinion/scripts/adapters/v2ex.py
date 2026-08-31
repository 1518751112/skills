"""Public V2EX/Sov2ex collector; no credentials or third-party packages."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

V2EX_API = "https://www.v2ex.com/api/topics"
SOV2EX_API = "https://www.sov2ex.com/api/search"
USER_AGENT = "public-opinion-monitor/1.0"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024


def _get_json(url: str) -> Any:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(request, timeout=15) as response:
        body = response.read(MAX_RESPONSE_BYTES + 1)
    if len(body) > MAX_RESPONSE_BYTES:
        raise ValueError("response exceeds 2 MiB limit")
    return json.loads(body.decode("utf-8"))


def _topic_url(topic: dict[str, Any]) -> str:
    url = topic.get("url")
    if isinstance(url, str) and url:
        return url
    topic_id = topic.get("id") or topic.get("topic_id")
    return f"https://www.v2ex.com/t/{topic_id}" if topic_id else ""


def _normalize(topic: dict[str, Any]) -> dict[str, Any] | None:
    node = topic.get("node")
    member = topic.get("member") or topic.get("user")
    url = _topic_url(topic)
    if not url:
        return None
    metrics: dict[str, int] = {}
    replies = topic.get("replies", topic.get("reply_count"))
    if isinstance(replies, int):
        metrics["comment_count"] = replies
    return {
        "platform": "v2ex",
        "external_id": str(topic.get("id") or topic.get("topic_id") or ""),
        "url": url,
        "title": str(topic.get("title") or ""),
        "content": str(topic.get("content") or topic.get("content_rendered") or ""),
        "node": str((node.get("name") if isinstance(node, dict) else node if isinstance(node, str) else "") or topic.get("node_name") or ""),
        "author": str((member.get("username") if isinstance(member, dict) else member if isinstance(member, str) else "") or topic.get("username") or ""),
        "published_at": topic.get("created") or topic.get("created_at"),
        "metrics": metrics,
        "raw": topic,
    }


def _search_hits(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    hits = payload.get("hits")
    if isinstance(hits, dict):
        hits = hits.get("hits")
    for candidate in (hits, payload.get("data"), payload.get("items"), payload.get("result")):
        if isinstance(candidate, list):
            return [item.get("_source", item) for item in candidate if isinstance(item, dict)]
    return []


def collect(request: dict[str, Any]) -> list[dict[str, Any]]:
    """Collect one configured V2EX mode and return normalized public posts."""
    mode = request["mode"]
    limit = max(1, min(int(request.get("limit", 20)), 100))
    if mode == "hot":
        payload = _get_json(f"{V2EX_API}/hot.json")
    elif mode == "latest":
        payload = _get_json(f"{V2EX_API}/latest.json")
    elif mode == "node":
        node = request.get("node")
        if not isinstance(node, str) or not node:
            raise ValueError("node mode requires a non-empty node")
        payload = _get_json(f"{V2EX_API}/show.json?{urlencode({'node_name': node})}")
    elif mode == "search":
        query = request.get("query")
        if not isinstance(query, str) or not query:
            raise ValueError("search mode requires a non-empty query")
        params = {"q": query, "sort": "created", "order": 0, "from": 0, "size": limit, "node": request.get("node", "undefined"), "lte": 0, "gte": 0}
        payload = _search_hits(_get_json(f"{SOV2EX_API}?{urlencode(params)}"))
    else:
        raise ValueError(f"unsupported V2EX mode: {mode}")
    return [post for item in payload[:limit] if (post := _normalize(item))]
