"""Common public-opinion client: collect, URL-deduplicate, and persist decisions."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from adapters import v2ex

ADAPTERS = {"v2ex": v2ex.collect}
REVIEW_FIELDS = (
    "platform",
    "external_id",
    "url",
    "title",
    "content",
    "node",
    "author",
    "published_at",
    "metrics",
)


def canonical_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"invalid post URL: {value!r}")
    return urlunsplit(("https", parsed.netloc.lower(), parsed.path.rstrip("/"), "", ""))


class Store:
    def __init__(self, database: str) -> None:
        database_path = Path(database)
        database_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(database_path)
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS posts (
                url TEXT PRIMARY KEY, platform TEXT NOT NULL, external_id TEXT,
                title TEXT NOT NULL, content TEXT, node TEXT, author TEXT,
                published_at TEXT, metrics_json TEXT NOT NULL, raw_json TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending', decision_reason TEXT,
                labels_json TEXT, first_seen_at TEXT NOT NULL, last_seen_at TEXT NOT NULL
            )"""
        )

    def known(self, url: str) -> bool:
        return self.connection.execute("SELECT 1 FROM posts WHERE url = ?", (canonical_url(url),)).fetchone() is not None

    def upsert_post(self, post: dict[str, Any]) -> None:
        now = datetime.now(UTC).isoformat()
        self.connection.execute(
            """INSERT INTO posts (url, platform, external_id, title, content, node, author, published_at, metrics_json, raw_json, first_seen_at, last_seen_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(url) DO UPDATE SET platform=excluded.platform, external_id=excluded.external_id,
               title=excluded.title, content=excluded.content, node=excluded.node, author=excluded.author,
               published_at=excluded.published_at, metrics_json=excluded.metrics_json, raw_json=excluded.raw_json,
               last_seen_at=excluded.last_seen_at""",
            (canonical_url(post["url"]), post["platform"], post["external_id"], post["title"], post["content"], post["node"], post["author"], str(post["published_at"] or ""), json.dumps(post["metrics"], ensure_ascii=False), json.dumps(post["raw"], ensure_ascii=False), now, now),
        )

    def review(self, item: dict[str, Any]) -> None:
        decision = item.get("decision")
        if decision not in {"matched", "rejected", "pending"}:
            raise ValueError("decision must be matched, rejected, or pending")
        cursor = self.connection.execute(
            "UPDATE posts SET status=?, decision_reason=?, labels_json=? WHERE url=?",
            (decision, item.get("reason"), json.dumps(item.get("labels", []), ensure_ascii=False), canonical_url(item["url"])),
        )
        if cursor.rowcount != 1:
            raise ValueError(f"decision URL is not in the database: {item['url']}")

    def commit(self) -> None:
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()


def scan(config: dict[str, Any], include_known: bool = False) -> dict[str, Any]:
    platform = config.get("platform")
    if platform not in ADAPTERS:
        raise ValueError(f"unsupported platform: {platform!r}")
    database = config.get("database", "public-opinion.sqlite3")
    filter_known = bool(config.get("filter_known", True)) and not include_known
    store = Store(database)
    fetched = known_filtered = 0
    returned: list[dict[str, Any]] = []
    seen_now: set[str] = set()
    try:
        for request in config.get("requests", []):
            for post in ADAPTERS[platform](request):
                fetched += 1
                url = canonical_url(post["url"])
                known = url in seen_now or store.known(url)
                seen_now.add(url)
                store.upsert_post(post)
                if filter_known and known:
                    known_filtered += 1
                else:
                    returned.append({field: post[field] for field in REVIEW_FIELDS})
        store.commit()
    finally:
        store.close()
    return {"posts": returned, "counts": {"fetched": fetched, "returned": len(returned), "known_filtered": known_filtered}}


def main() -> None:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    scan_parser = commands.add_parser("scan")
    scan_parser.add_argument("--config", required=True, type=Path)
    scan_parser.add_argument("--include-known", action="store_true")
    scan_parser.add_argument("--titles", action="store_true")
    review_parser = commands.add_parser("review")
    review_parser.add_argument("--database", required=True)
    review_parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "scan":
        result = scan(json.loads(args.config.read_text(encoding="utf-8")), args.include_known)
        if args.titles:
            result["posts"] = [{"title": post["title"], "url": post["url"]} for post in result["posts"]]
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    decisions = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(decisions, list):
        raise ValueError("decision input must be a JSON array")
    store = Store(args.database)
    try:
        for item in decisions:
            store.review(item)
        store.commit()
    finally:
        store.close()


if __name__ == "__main__":
    main()
