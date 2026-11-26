#!/usr/bin/env python3
"""Write feed.xml, a podcast RSS feed, for a folder of episodes. Plain Python, no installs.

  build_feed.py <feed folder> --title "Sam's Course" --base-url https://sam.github.io/my-course-feed
      First run: saves the title and address in <feed folder>/feed.json.

  build_feed.py <feed folder>
      Later runs: rebuilds feed.xml from every episodes/<slug>.json (written by make_audio.py).

The feed folder then holds feed.json, feed.xml and episodes/. Upload the whole folder to the
place --base-url points at; the feed's address is <base-url>/feed.xml.
"""
import argparse, json, os, sys
from email.utils import parsedate_to_datetime
from xml.sax.saxutils import escape, quoteattr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("feed_dir")
    ap.add_argument("--title")
    ap.add_argument("--base-url", help="public address of this folder, no trailing slash")
    ap.add_argument("--description")
    a = ap.parse_args()

    d = os.path.abspath(os.path.expanduser(a.feed_dir))
    os.makedirs(os.path.join(d, "episodes"), exist_ok=True)
    cfg_path = os.path.join(d, "feed.json")
    cfg = {}
    if os.path.exists(cfg_path):
        with open(cfg_path, encoding="utf-8") as f:
            cfg = json.load(f)
    if a.title: cfg["title"] = a.title
    if a.base_url: cfg["base_url"] = a.base_url.rstrip("/")
    if a.description: cfg["description"] = a.description
    if not (cfg.get("title") and cfg.get("base_url")):
        sys.exit("first run needs --title and --base-url")
    if not cfg["base_url"].startswith("https://"):
        sys.exit("--base-url must start with https:// (podcast apps refuse plain http)")
    cfg.setdefault("description", "A personal paired course.")
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

    eps = []
    for name in sorted(os.listdir(os.path.join(d, "episodes"))):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(d, "episodes", name), encoding="utf-8") as f:
            e = json.load(f)
        mp3 = os.path.join(d, "episodes", e["file"])
        if not os.path.exists(mp3):
            print(f"skipped {name}: {e['file']} is missing")
            continue
        e["bytes"] = os.path.getsize(mp3)
        eps.append(e)
    eps.sort(key=lambda e: parsedate_to_datetime(e["pubDate"]), reverse=True)

    base = cfg["base_url"]
    items = []
    for e in eps:
        s = int(e.get("duration", 0))
        items.append(f"""    <item>
      <title>{escape(e['title'])}</title>
      <description>{escape(e.get('description', ''))}</description>
      <guid isPermaLink="false">{escape(e['slug'])}</guid>
      <pubDate>{escape(e['pubDate'])}</pubDate>
      <enclosure url={quoteattr(f"{base}/episodes/{e['file']}")} length="{e['bytes']}" type="audio/mpeg"/>
      <itunes:duration>{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}</itunes:duration>
    </item>""")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>{escape(cfg['title'])}</title>
    <link>{escape(base)}</link>
    <description>{escape(cfg['description'])}</description>
    <language>en</language>
    <itunes:block>Yes</itunes:block>
    <itunes:explicit>false</itunes:explicit>
{chr(10).join(items)}
  </channel>
</rss>
"""
    with open(os.path.join(d, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"feed.xml: {len(eps)} episode(s). Feed address once uploaded: {base}/feed.xml")


if __name__ == "__main__":
    main()
