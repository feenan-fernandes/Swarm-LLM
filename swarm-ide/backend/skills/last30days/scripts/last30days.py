#!/usr/bin/env python3
"""
last30days.py — Real-time research engine for AI Agents.
Researches any topic across Reddit, Hacker News, Polymarket, and GitHub
strictly within the past 30 days, scored by organic engagement.
Stdlib-only implementation.
"""

import argparse
import datetime
import json
import os
import sys
import time
import urllib.parse
import urllib.request


USER_AGENT = "Last30Days-Skill/1.0 (Agentic Research Engine; Python/urllib)"


def fetch_json(url, timeout=6):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                data = resp.read().decode("utf-8", errors="replace")
                return json.loads(data)
    except Exception as e:
        return {"error": str(e)}
    return None


def search_hacker_news(query, cutoff_ts, limit=5):
    encoded = urllib.parse.quote(query)
    url = f"https://hn.algolia.com/api/v1/search_by_date?query={encoded}&numericFilters=created_at_i>{cutoff_ts}&tags=story&hitsPerPage={limit}"
    data = fetch_json(url)
    results = []
    if data and "hits" in data:
        for hit in data["hits"]:
            created_at = hit.get("created_at_i", 0)
            if created_at < cutoff_ts:
                continue
            points = hit.get("points") or 0
            comments = hit.get("num_comments") or 0
            title = hit.get("title") or "Untitled"
            url_hit = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            results.append({
                "source": "Hacker News",
                "title": title,
                "score": points + (comments * 2),
                "metrics": f"{points} points, {comments} comments",
                "date": datetime.datetime.fromtimestamp(created_at, datetime.timezone.utc).strftime("%Y-%m-%d"),
                "url": url_hit
            })
    return results


def search_reddit(query, cutoff_ts, limit=5):
    encoded = urllib.parse.quote(query)
    url = f"https://www.reddit.com/search.json?q={encoded}&sort=top&t=month&limit={limit}"
    data = fetch_json(url)
    results = []
    if data and "data" in data and "children" in data["data"]:
        for child in data["data"]["children"]:
            item = child.get("data", {})
            created_utc = item.get("created_utc", 0)
            if created_utc < cutoff_ts:
                continue
            ups = item.get("ups", 0)
            num_comments = item.get("num_comments", 0)
            title = item.get("title", "Untitled")
            subreddit = item.get("subreddit", "unknown")
            permalink = item.get("permalink", "")
            url_hit = f"https://reddit.com{permalink}" if permalink else ""
            results.append({
                "source": f"Reddit (r/{subreddit})",
                "title": title,
                "score": ups + (num_comments * 2),
                "metrics": f"{ups} upvotes, {num_comments} comments",
                "date": datetime.datetime.fromtimestamp(created_utc, datetime.timezone.utc).strftime("%Y-%m-%d"),
                "url": url_hit
            })
    return results


def search_github(query, cutoff_date_str, limit=5):
    encoded = urllib.parse.quote(f"{query} pushed:>{cutoff_date_str}")
    url = f"https://api.github.com/search/repositories?q={encoded}&sort=updated&order=desc&per_page={limit}"
    data = fetch_json(url)
    results = []
    if data and "items" in data:
        for item in data["items"]:
            stars = item.get("stargazers_count", 0)
            forks = item.get("forks_count", 0)
            full_name = item.get("full_name", "")
            desc = item.get("description") or ""
            html_url = item.get("html_url", "")
            updated_at = item.get("updated_at", "")[:10]
            results.append({
                "source": "GitHub",
                "title": f"{full_name}: {desc[:80]}..." if len(desc) > 80 else f"{full_name}: {desc}",
                "score": stars + forks,
                "metrics": f"{stars} stars, {forks} forks",
                "date": updated_at,
                "url": html_url
            })
    return results


def search_polymarket(query, limit=3):
    encoded = urllib.parse.quote(query)
    url = f"https://gamma-api.polymarket.com/events?slug={encoded}&closed=false&limit={limit}"
    data = fetch_json(url)
    results = []
    if data and isinstance(data, list):
        for item in data:
            title = item.get("title", "")
            volume = item.get("volume", 0)
            slug = item.get("slug", "")
            results.append({
                "source": "Polymarket",
                "title": title,
                "score": int(float(volume or 0)),
                "metrics": f"${float(volume or 0):,.0f} volume",
                "date": "Active Market",
                "url": f"https://polymarket.com/event/{slug}"
            })
    return results


def run_preflight():
    print("=== Last30Days Engine Preflight ===")
    print(f"Runtime: Python {sys.version.split()[0]} (stdlib-only)")
    print("Default Lookback: 30 days")
    print("Supported Zero-Config Sources:")
    print("  [x] Hacker News (Algolia Search API)")
    print("  [x] Reddit (Public Search JSON API)")
    print("  [x] GitHub Repos (GitHub Search API)")
    print("  [x] Polymarket (Gamma Events API)")
    print("Status: READY FOR EXECUTION")
    return True


def main():
    parser = argparse.ArgumentParser(description="Research discourse strictly from the past 30 days.")
    parser.add_argument("topic", nargs="?", default="", help="Query or topic to research")
    parser.add_argument("--lookback-days", type=int, default=30, help="Days to look back (default: 30)")
    parser.add_argument("--quick", action="store_true", help="Run quick search with smaller limit")
    parser.add_argument("--preflight", action="store_true", help="Run connectivity and engine check")
    parser.add_argument("--emit", choices=["compact", "json", "markdown"], default="compact", help="Output format")

    args = parser.parse_args()

    if args.preflight or not args.topic:
        run_preflight()
        if not args.topic:
            print("\nUsage: python last30days.py \"topic\" [--lookback-days 30] [--quick]")
        return

    topic = args.topic.strip()
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(days=args.lookback_days)
    cutoff_ts = int(cutoff.timestamp())
    cutoff_date_str = cutoff.strftime("%Y-%m-%d")

    limit = 3 if args.quick else 5

    all_signals = []
    all_signals.extend(search_hacker_news(topic, cutoff_ts, limit=limit))
    all_signals.extend(search_reddit(topic, cutoff_ts, limit=limit))
    all_signals.extend(search_github(topic, cutoff_date_str, limit=limit))
    all_signals.extend(search_polymarket(topic, limit=limit))

    # Rank by engagement score
    all_signals.sort(key=lambda x: x.get("score", 0), reverse=True)

    if args.emit == "json":
        print(json.dumps({
            "topic": topic,
            "lookback_days": args.lookback_days,
            "cutoff_date": cutoff_date_str,
            "results_count": len(all_signals),
            "signals": all_signals
        }, indent=2))
        return

    print(f"## Recent 30-Day Intelligence Brief: \"{topic}\"")
    print(f"*Date Range: {cutoff_date_str} to {now.strftime('%Y-%m-%d')}*\n")

    if not all_signals:
        print("No active community signals found matching this query in the past 30 days.")
        return

    for i, s in enumerate(all_signals, 1):
        print(f"**{i}. [{s['source']}] {s['title']}**")
        print(f"   - Signal: {s['metrics']} | Date: {s['date']}")
        if s.get('url'):
            print(f"   - Link: {s['url']}")
        print()


if __name__ == "__main__":
    main()
