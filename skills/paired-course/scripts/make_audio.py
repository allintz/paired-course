#!/usr/bin/env python3
"""Turn a spoken-word script into a podcast episode: <slug>.mp3 and <slug>.json.

Run with the Python that setup_audio.sh prepared (~/.cache/kokoro/venv/bin/python):

  make_audio.py script.txt --check
      Lint only: word count, expected length, and lines the voice may mangle.

  make_audio.py script.txt --slug w1d1-national-emergencies-act \\
      --title "W1 D1: The emergency that never ends" \\
      --description "One or two plain sentences." --out <feed folder>/episodes

In the script, blank lines separate paragraphs (short pause). A line with only
--- is a longer pause, for a change of section.
"""
import argparse, json, os, re, subprocess, sys, tempfile
from datetime import datetime, timezone
from email.utils import format_datetime

KOKORO_DIR = os.environ.get("KOKORO_DIR", os.path.expanduser("~/.cache/kokoro"))
os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("PATH", "")
WORDS_PER_MIN = 150
PAUSE = "[[pause]]"


def clean_for_speech(text):
    """Remove things a voice would read badly, line by line."""
    lines = []
    for line in text.splitlines():
        if re.fullmatch(r"\s*([-*_]\s*){3,}", line):
            lines.append(PAUSE)
            continue
        marked = bool(re.match(r"\s{0,3}(#{1,6}\s|[-*•]\s+|\d+[.)]\s+)", line))
        line = re.sub(r"^\s{0,3}(#{1,6}\s*|[-*•]\s+)", "", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)        # markdown links -> label
        line = re.sub(r"https?://\S+", "", line)                     # bare URLs
        line = re.sub(r"[*`]+|(?<!\w)_+|_+(?!\w)", "", line)         # emphasis marks
        line = re.sub(r"(?<=\d)\s*[–—-]\s*(?=\d)", " to ", line)     # 5–10 -> 5 to 10
        line = re.sub(r"\s*[–—]\s*", ", ", line)                     # other dashes -> pause
        line = line.replace("%", " percent").replace("&", " and ")
        line = re.sub(r"[ \t]+", " ", line).strip()
        line = re.sub(r"\s+([,.;:!?])", r"\1", line)
        if marked and line and line[-1] not in ".!?:":
            line += "."
        lines.append(line)
    return "\n".join(lines).rstrip()


def paragraphs(text, max_chars=1200):
    """Short chunks keep the voice's pacing steady: split on blank lines, then sentences."""
    out = []
    text = text.replace(PAUSE, f"\n\n{PAUSE}\n\n")
    for para in re.split(r"\n\s*\n", text):
        para = " ".join(para.split())
        if not para:
            continue
        if para == PAUSE:
            out.append(PAUSE)
            continue
        cur = ""
        for sent in re.findall(r"[^.!?]+[.!?]+[\"')]*\s*|[^.!?]+$", para):
            if cur and len(cur) + len(sent) > max_chars:
                out.append(cur.strip()); cur = ""
            cur += sent
        if cur.strip():
            out.append(cur.strip())
    return out


def lint(text):
    """Things the voice is likely to mangle. Advisory: fix them in the script."""
    checks = [
        (r"[$€£]\s?\d", "currency symbol (write 'three million dollars')"),
        (r"[/~→|<>=+^\\\[\]{}#@]", "symbol the voice may read oddly"),
        (r"\d+\.\d+|\d{1,3}(,\d{3})+", "precise figure (round it and say it in words)"),
        (r"\b(e\.g\.|i\.e\.|etc\.|vs\.?)(?=\s|$)", "abbreviation (write it out)"),
        (r"\b[A-Z]{3,}\b", "initialism (space the letters if it should be spelled out)"),
        (r"\([^)]{0,80}\)", "parenthetical (say it as its own sentence)"),
    ]
    found = []
    for n, line in enumerate(text.splitlines(), 1):
        if line == PAUSE:
            continue
        for pat, why in checks:
            m = re.search(pat, line)
            if m:
                found.append(f"  line {n}: {why}: ...{line[max(0, m.start()-25):m.end()+25].strip()}...")
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--slug", help="lowercase letters, digits and hyphens; the file name and the feed id")
    ap.add_argument("--title")
    ap.add_argument("--description")
    ap.add_argument("--out", help="folder for the mp3 and json, normally <feed folder>/episodes")
    ap.add_argument("--voice", default="af_heart")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--check", action="store_true", help="lint the script and stop")
    a = ap.parse_args()

    with open(os.path.expanduser(a.script), encoding="utf-8") as f:
        text = clean_for_speech(f.read())
    chunks = paragraphs(text)
    if not chunks:
        sys.exit("the script is empty")

    words = len(text.replace(PAUSE, " ").split())
    print(f"{words} words, expect about {words / WORDS_PER_MIN / a.speed:.1f} min")
    problems = lint(text)
    if problems:
        print(f"{len(problems)} thing(s) the voice may mangle:")
        print("\n".join(problems))
    if a.check:
        return
    if not (a.slug and a.title and a.description and a.out):
        sys.exit("--slug, --title, --description and --out are required")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", a.slug):
        sys.exit("--slug must be lowercase letters, digits and hyphens")

    import numpy as np
    import soundfile as sf
    from kokoro_onnx import Kokoro

    model = next((p for p in (os.path.join(KOKORO_DIR, n) for n in
                 ("kokoro-v1.0.onnx", "kokoro-v1.0.int8.onnx")) if os.path.exists(p)), None)
    if not model:
        sys.exit(f"no voice model in {KOKORO_DIR}: run setup_audio.sh")
    kokoro = Kokoro(model, os.path.join(KOKORO_DIR, "voices-v1.0.bin"))
    parts, rate = [], 24000
    for i, chunk in enumerate(chunks, 1):
        if chunk == PAUSE:
            parts.append(np.zeros(int(rate * 0.9), dtype=np.float32))  # section break
            continue
        print(f"  {i}/{len(chunks)} ({len(chunk)} chars)", flush=True)
        samples, rate = kokoro.create(chunk, voice=a.voice, speed=a.speed, lang="en-us")
        if len(samples) < rate * len(chunk) / 60:   # under a third of normal speaking pace
            sys.exit(f"chunk {i} came out far too short; the voice dropped text: {chunk[:80]!r}")
        parts.append(samples.astype(np.float32))
        parts.append(np.zeros(int(rate * 0.5), dtype=np.float32))  # pause between paragraphs

    out = os.path.abspath(os.path.expanduser(a.out))
    os.makedirs(out, exist_ok=True)
    mp3 = os.path.join(out, f"{a.slug}.mp3")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav = tmp.name
    try:
        sf.write(wav, np.concatenate(parts), rate)
        # Even loudness (the usual level for mono speech) and a sample rate every player accepts.
        subprocess.run(["ffmpeg", "-y", "-i", wav, "-af", "loudnorm=I=-19:TP=-1.5:LRA=11",
                        "-ar", "44100", "-ac", "1", "-codec:a", "libmp3lame", "-b:a", "64k",
                        "-metadata", f"title={a.title}", mp3], check=True, capture_output=True)
        dur = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3],
            check=True, capture_output=True, text=True).stdout.strip())
    finally:
        os.unlink(wav)

    # Keep the original publish date when an episode is made again.
    meta_path = os.path.join(out, f"{a.slug}.json")
    pub = format_datetime(datetime.now(timezone.utc), usegmt=True)
    if os.path.exists(meta_path):
        with open(meta_path, encoding="utf-8") as f:
            pub = json.load(f).get("pubDate", pub)
    meta = {"slug": a.slug, "title": a.title, "description": a.description, "pubDate": pub,
            "file": f"{a.slug}.mp3", "bytes": os.path.getsize(mp3), "duration": round(dur)}
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    print(f"Wrote {mp3} ({meta['bytes']/1e6:.1f} MB, {dur/60:.1f} min)")
    expected = words / WORDS_PER_MIN / a.speed
    if not 0.6 * expected <= dur / 60 <= 1.6 * expected:
        print(f"WARNING: duration is far from the expected {expected:.1f} min; listen before publishing")


if __name__ == "__main__":
    main()
