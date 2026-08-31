---
name: public-opinion-monitor
description: Monitor public social-platform discussions for a brand, topic, incident, job market, or keyword. Use this skill whenever the user asks to watch public opinion, collect social posts, find negative discussion, search current social conversations or remote jobs, track hot/latest/posts by community, or deduplicate monitored posts before AI review. It currently supports V2EX and is designed to add one adapter per platform without changing the common client.
---

# Public-opinion monitor

Use public endpoints only, follow the platform's terms and rate limits, and do not attempt to bypass login, access controls, or anti-bot measures.

## Workflow

1. Convert the user's monitoring request into one or more collection requests: `hot`, `latest`, `node`, or `search`.
2. Run `scripts/client.py scan` with a JSON configuration. It normalizes posts, stores newly seen URLs in SQLite, and prints only URLs that have not previously been collected by default.
3. Judge only the returned posts against the user's stated criteria. The client retains the full provider response locally but deliberately sends AI only normalized fields, so raw HTML and duplicate metadata do not consume tokens.
4. Save every AI decision with `scripts/client.py review`. Use `matched` for relevant posts and `rejected` otherwise; include a short reason and optional labels.
5. Report the matched posts with title, URL, content excerpt, available metrics, and reason. State when no new posts were found.

The default is URL deduplication. Do not set `filter_known` to `false` or pass `--include-known` unless the user explicitly asks to include previously collected posts.

## Configuration

Create a JSON file such as:

```json
{
  "platform": "v2ex",
  "database": "public-opinion.sqlite3",
  "filter_known": true,
  "requests": [
    {"mode": "hot", "limit": 20},
    {"mode": "latest", "limit": 20},
    {"mode": "node", "node": "python", "limit": 20},
    {"mode": "search", "query": "品牌名", "limit": 20}
  ]
}
```

Run it from this skill directory:

```powershell
python scripts/client.py scan --config monitor.json
```

`scan` prints one JSON object containing `posts` (the items eligible for AI review) and counts. It uses the SQLite file named by `database`; no records are fabricated when an endpoint returns no data.

Use `--titles` when the user asks only for titles. Render each title as a Markdown link using its returned URL. On Windows, the client emits UTF-8 JSON so Chinese titles can be printed safely.

```powershell
python scripts/client.py scan --config monitor.json --titles
```

## Search relevance

Search results are candidates, not conclusions. For a multi-condition request such as “remote UI designer hiring,” inspect title and content for every condition before labeling it matched:

- `matched`: an employer or client is offering a UI/UX/design role and the stated work arrangement is remote.
- `rejected`: only some keywords match, or the post is unrelated.
- `rejected`: a designer's own job-seeking/portfolio post when the user asked for openings; mention it separately only if it could still be useful.

When the user explicitly asks to show all collected results, do not apply this relevance filter: return every title and URL, including previously stored posts if they also explicitly asked to disable deduplication.

## Saving AI decisions

After judging the returned posts, write a JSON array:

```json
[
  {
    "url": "https://www.v2ex.com/t/123",
    "decision": "matched",
    "reason": "Reports a reproducible outage affecting the monitored product.",
    "labels": ["outage", "negative"]
  }
]
```

Then save it:

```powershell
python scripts/client.py review --database public-opinion.sqlite3 --input decisions.json
```

Use `pending` only when the criteria do not permit a decision. Never represent a pending item as matched.

## V2EX modes

- `hot`: V2EX public hot-topics API.
- `latest`: V2EX public latest-topics API.
- `node`: latest topics in one V2EX node; omit the request if the requested platform has no equivalent board.
- `search`: Sov2ex public search API. It supports `query`; V2EX's official public API does not provide full-text search.

The normalized `metrics` field contains only values received from a source (for V2EX, typically `comment_count`). New adapters belong in `scripts/adapters/` and must return the same normalized fields; register them in `scripts/client.py`.

## Verification

Run the local deduplication check after changing the client or store:

```powershell
python -m unittest discover -s tests -v
```
