# Paired course

A skill for Claude (or any AI assistant that can follow written instructions) that sets up and runs a personal course for a busy person:

- **Morning:** a 10 to 15 minute podcast episode on one idea.
- **Evening:** five quiz cards on that same idea in [WonkoLingo](https://wonkolingo.com), plus reviews of earlier ones.
- **Weekly:** a five-minute check-in. What came up at work that you didn't know enough about? Where did you feel out of your depth? The next week is planned from the answers.

The learner listens, taps and answers a few questions a week. The assistant does the rest: the interview, the outline, fact-checked episode scripts, and the cards.

## What's here

| File | What it is |
|---|---|
| `skills/paired-course/SKILL.md` | The skill: setup interview, weekly plan, making a week, check-ins |
| `skills/paired-course/references/wonkolingo.md` | Instructions for an AI to write a custom WonkoLingo course and get it into the app |
| `skills/paired-course/references/podcast.md` | Instructions for an AI to make the audio and set up a private podcast feed (RSS) on free hosting |
| `skills/paired-course/scripts/` | `setup_audio.sh` (installs a free local voice model), `make_audio.py` (script to MP3), `build_feed.py` (writes the feed) |
| `skills/paired-course/references/templates.md` | The shape of the learner's profile, outline, weekly plan, fact sheets and log |

## Using it

**Claude Code:** copy `skills/paired-course` into `~/.claude/skills/`, then say "set up a paired course for me".

**Claude apps:** zip the `skills/paired-course` folder and add it under Settings, Capabilities, Skills. Or attach `SKILL.md` and the reference files to a project.

**Any other assistant:** give it the files in `skills/paired-course` and ask it to follow `SKILL.md`.

You also need a free WonkoLingo account to add your course, and some way to listen:

- **With an assistant that can run commands on your computer** (such as Claude Code), a free voice model on your machine makes each episode as an MP3. You upload the week's recordings to WonkoLingo with the cards, and they play there: the app holds each lesson's cards until you have listened, and the iPhone app sends a notification each morning with the day's episode. It can also set up a podcast feed on free hosting if you would rather use your podcast app.
- **With a chat-only assistant**, it gives you each script to play with a read-aloud app.

## Honest limits

- Scripts and cards are fact-checked by the AI against sources it links, not by a person. Treat them as a good briefing, not an authority.
- The podcast feed is unlisted, not private: anyone with its address can listen.
- The audio setup script has been run on one Mac. It should work on Linux too but has not been tried there.
- Adding each week's cards and recordings to WonkoLingo is one upload by hand. The assistant cannot do it for you.
- Episodes in WonkoLingo play on the Today screen only, and need a connection. Playing with the phone locked is new and has not been tried on many phones.
- The assistant cannot see your quiz results unless you tell it how the week went.
