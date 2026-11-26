# Making the podcast and setting up the feed

For an AI assistant that can run commands on the learner's computer. It covers turning a script into audio, hosting it, and giving the learner a private podcast feed that their podcast app follows, so new episodes just appear. Everything here is free.

If you cannot run commands, skip to "No command line" at the end.

`SKILL_DIR` below is the folder that holds `SKILL.md`.

## What the learner ends up with

One web address ending in `feed.xml`. They add it to their podcast app once. After that, each episode you publish shows up on their phone like any other show.

Tell the learner before you set it up: **the feed is unlisted, not private.** Nobody will find it by searching, and the feed asks podcast directories not to list it, but anyone who has the address can listen. So scripts and descriptions must never include anything personal about them.

## One-time setup

### 1. Audio tools

```bash
SKILL_DIR/scripts/setup_audio.sh
```

This installs Kokoro, a free open-source voice model that runs on their computer (about 120 MB, macOS or Linux), into `~/.cache/kokoro`. It needs `ffmpeg` and Python 3 and says how to get ffmpeg if it is missing. If the install fails on a very new Python, install `uv` (https://docs.astral.sh/uv/) and run it again; the script then uses Python 3.12. On Windows, run all of this inside WSL.

On a fresh Ubuntu or Debian machine, install `ffmpeg` and `python3-venv` first. The setup, MP3 generation, and RSS feed were tested together on Ubuntu 24.04 (ARM64).

From then on, run the audio script with `~/.cache/kokoro/venv/bin/python`.

### 2. A place to host the files

Podcast apps fetch the feed and the audio from the web, so the files need a public https address. Pick one with the learner:

**GitHub Pages** (simplest if they have a GitHub account):

1. Create a new public repository, for example `my-course-feed`, and clone it. This folder is the feed folder.
2. In the repository on github.com: Settings, Pages, "Deploy from a branch", branch `main`, folder `/ (root)`.
3. The base address is `https://<username>.github.io/my-course-feed`.

GitHub Pages on a free account needs a public repository, and sites are meant to stay under roughly 1 GB. A 15-minute episode is about 7 MB, so that is room for over a hundred; delete old ones if it fills up. Check GitHub's current limits if in doubt.

**Cloudflare R2** (if they have a Cloudflare account):

1. Create a bucket, and under its Settings turn on the public development URL (or connect a domain they own).
2. The base address is the public URL Cloudflare shows, for example `https://pub-xxxxxxxx.r2.dev`.
3. Upload with `npx wrangler r2 object put <bucket>/<path> --file <local file> --remote`, after `npx wrangler login`.

Any other static host works the same way: it only has to serve the feed folder over https.

### 3. Create the feed

```bash
python3 SKILL_DIR/scripts/build_feed.py <feed folder> --title "<Name>'s Course" --base-url <base address>
```

This saves the title and address in `<feed folder>/feed.json` and writes an empty `feed.xml`. Record the feed folder and the feed address (`<base address>/feed.xml`) in the learner's `profile.md`.

## Each episode

1. **Check the script.**
   ```bash
   ~/.cache/kokoro/venv/bin/python SKILL_DIR/scripts/make_audio.py <script.txt> --check
   ```
   It prints the word count, the expected length, and every line the voice is likely to mangle (symbols, precise figures, abbreviations, initialisms, brackets). Fix those in the script and run it again until anything left is deliberate. Spell initialisms the voice should say letter by letter with spaces ("F B I"); if the voice is likely to mispronounce a name, spell it the way it sounds.

2. **Make the audio.**
   ```bash
   ~/.cache/kokoro/venv/bin/python SKILL_DIR/scripts/make_audio.py <script.txt> \
     --slug w1d1-short-name --title "W1 D1: Episode title" \
     --description "One or two plain sentences." --out <feed folder>/episodes
   ```
   It writes `<slug>.mp3` and `<slug>.json` into `episodes/`. Expect roughly a minute of work per ten minutes of audio on a recent laptop. The slug is the episode's permanent id in the feed: lowercase letters, digits and hyphens, never reused for a different episode. Running it again with the same slug replaces that episode and keeps its date. If it stops or warns about the length, the voice dropped or garbled something; fix the line it names. `--voice` picks another Kokoro voice (default `af_heart`) and `--speed 1.1` talks faster.

3. **Rebuild the feed.**
   ```bash
   python3 SKILL_DIR/scripts/build_feed.py <feed folder>
   ```

4. **Upload.** On GitHub Pages, commit and push the feed folder:
   ```bash
   cd <feed folder> && git add -A && git commit -m "Add episode" && git push
   ```
   On R2, upload the new `episodes/<slug>.mp3` and then `feed.xml` (audio first, so the feed never points at a missing file).

5. **Verify before telling the learner it is out.** Fetch `<base address>/feed.xml` and check the new episode is in it, then request the audio address and check it answers with status 200 and the right size. GitHub Pages can take a minute or two to update.
   ```bash
   curl -s <base address>/feed.xml | grep -c "<item>"
   ```
   ```bash
   curl -sI <base address>/episodes/<slug>.mp3 | head -1
   ```

A whole week can be made at once: steps 1 and 2 for each day, then steps 3 to 5 once. Podcast apps order episodes by date, so make them in day order.

## Subscribing (the learner does this once)

Give them the feed address and these steps. Menu wording changes between app versions, so describe the goal ("add a show by its address") if a label does not match.

- **Apple Podcasts:** Library, the "..." menu at the top, "Follow a Show by URL", paste the address.
- **Overcast:** the "+" button, "Add URL", paste.
- **Pocket Casts:** paste the address into the search box.
- **Spotify** cannot follow a private feed address. Use one of the others.

New episodes can take up to an hour to appear; pulling down to refresh in the app is faster.

## Without hosting

If the learner does not want anything on the web, do steps 1 and 2 only and have them move the MP3s to their phone (AirDrop, a synced folder, a messaging app to themselves). It works, but it is a manual step every week, so offer the feed first.

## No command line

In a chat with no way to run commands, you cannot make audio. Hand over each script as plain text, one per day, titled in order, and have the learner play it with a read-aloud app or their phone's screen reader. Still write for the ear, and still pair every script with its cards.
