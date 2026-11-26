---
name: paired-course
description: Set up and run a personal "paired course" for a busy person - a short podcast episode each morning, WonkoLingo quiz cards on the same material each evening, and a five-minute check-in each week that steers what comes next. Use this whenever someone wants to keep learning about a topic with little effort, asks for a daily learning podcast with quizzes, a course built around their job or what they feel out of their depth on, a custom WonkoLingo course made for them, a "learning loop", or says things like "set up my course", "plan next week's episodes", "weekly check-in", "what should I learn next", "is this course still right for me", or "make this week's episodes and cards". Also use it to resume or adjust a paired course that already exists, even if the person only mentions the podcast half or the WonkoLingo half.
---

# Paired course

A paired course is for someone who has almost no spare time but wants to keep getting better at something they care about. They listen for 10 to 15 minutes in the morning and answer quiz cards on the same material in the evening, in [WonkoLingo](https://wonkolingo.com), a free spaced-repetition quiz app that accepts custom courses. Hearing an idea and then having to recall it a few hours later is what makes it stick, so the two halves must always match.

They must also each work alone. People miss mornings. The app has no idea whether an episode was heard, so on a missed day the learner meets that day's cards cold. A card that only makes sense to someone who listened is a broken card: every card has to be answerable, and teach its idea in its explanation, for someone who has not heard the episode. The episode makes the cards easier; it is never what makes them possible.

Everything else is your job. The learner's whole effort is:

| When | What | How long |
|---|---|---|
| Once | Setup interview | about 10 minutes |
| Each morning | Listen to one episode | 10 to 15 minutes |
| Each evening | That episode's cards in WonkoLingo, plus reviews | about 5 minutes |
| Once a week | Check-in, then add the new week's cards to the app | about 5 minutes |

Protect that budget. Never give the learner homework, reading, or a form to fill in. If they skip a check-in, carry on with the outline as it stands. Ask for a decision only when the answer changes what gets made.

## Where things are

- `references/wonkolingo.md`: how to write the cards and get them into the learner's WonkoLingo. Read it before writing any card.
- `references/podcast.md`: how to turn a script into audio and give the learner a private podcast feed. Read it before making audio, unless this session already has its own podcast tool.
- `scripts/`: `setup_audio.sh`, `make_audio.py`, `build_feed.py`, used by `references/podcast.md`.
- `references/templates.md`: the shape of every file below.
- Each learner has a folder. Use `paired-course/<name>/` wherever this person keeps working files, and ask once if that is unclear. In a chat with no file access, keep the profile, outline and log in one document the person can paste back next time.

```
paired-course/<name>/
  profile.md        who they are, the goal, what they know, how they listen
  outline.md        the next four weeks; only the next week is firm
  log.md            one dated entry per check-in and per week made
  course.json       their whole WonkoLingo course so far (grows one unit a week)
  weeks/<YYYY>-W<nn>-<slug>/
    plan.md         five episode sketches and the review day; says "proposed" or "approved"
    d1-<slug>.facts.md, d1-<slug>.script.txt ... one pair per day
    unit.json       this week's cards, in the shape the app's Add questions takes
```

Read `profile.md`, `outline.md` and the last two `log.md` entries before doing anything for an existing learner. They are the only memory this course has.

## Which step are you on?

- No learner folder yet: run **Setup**.
- A new week needs making, or the learner asks what is next: run **Check-in**, then **Plan the week**, then **Make the week**.
- The learner says the course feels off: run **Check-in** now, whatever the day.
- Every fourth week: add the **Big check** to the check-in.

## Setup

The interview finds the gap between what the learner's work asks of them and what they know. Come prepared: read anything you already have about them and put your best guess in front of them, so most of their answers are "yes" or a correction. Ask in plain chat, a few questions at a time, and let them answer loosely or by voice.

Find out:

1. **Work.** What they do, and what decisions or documents they are responsible for.
2. **Goal.** What they want to be able to do that they can't do well now. Push for something you could observe ("review an AI bill and spot the weak enforcement section"), not a topic ("learn about legislation").
3. **Out of depth.** Recent moments where they felt lost: a meeting, a document, a question they couldn't answer. These are the best source of episodes.
4. **Already solid.** What to skip, so the course never explains what they know.
5. **Coming up.** Deadlines or events in the next two months they want to be ready for.
6. **Fit.** Episode length, which days they listen, and how many new cards an evening is comfortable (default 5).
7. **How they will listen.** See "Getting the episode to their ears" below. Settle this once and record it.
8. **WonkoLingo.** Whether they have the app and an account, and whether it already has a course on their topic (the app's course list shows them). If they already listen to another series in the same podcast feed, pick episode titles that cannot be confused with it.

Then write `profile.md` and `outline.md` from the templates, say the goal back in one sentence, show the four-week outline as a short list, and ask what to change. Only week one needs to be right.

## Cards: two ways to pair

Pick one per week and record it in `plan.md`.

- **Own course (the usual case).** Write five cards per episode: one lesson per episode, one unit per week, all in one personal course. Five matches WonkoLingo's default of five new cards a day per course, so each evening serves that morning's lesson with no setup. If the learner misses an evening, the cards fall a day behind the audio. If they miss a morning, the cards arrive anyway, which is why each one must work without the episode. Tell the learner both things at setup, and that listening late still helps: the episode then works as the review.
- **A course WonkoLingo already has.** If the app already has a course on the week's theme, the episodes can follow its lessons in order and no new cards are needed. The learner switches that course on in their daily mix. You need the course's cards to do this (the learner can tell you the lesson titles, or you may have the course file); every episode has to teach every card in its lesson. If you cannot see the cards, write an own course instead.

`references/wonkolingo.md` has the card rules, the file format, and the exact steps for the learner to add the course and each later week.

## Check-in

Start from what happened, so the learner reacts instead of remembering. If you have a way to read their WonkoLingo results, open with two or three plain observations ("You missed the two cards on sunset clauses twice each, and removed three about appropriations. Should I drop appropriations?"). If you don't, ask which cards kept tripping them up and whether they removed any. Ask whether they kept up with the episodes.

Then ask, conversationally and never as a form:

- What came up at work this week that you didn't know enough about?
- Where did you feel out of your depth?
- Which episode was most useful, and which could you have skipped?
- Too easy, too hard, or about right?
- Is anything coming up that you want to be ready for?
- Keep going, go deeper, or switch?

Three good answers are enough; stop when you have what you need. Write a dated entry in `log.md` (what the results showed, what they said in their words, what you changed), then update `profile.md` and `outline.md`. Things they said they need go to the front of the outline.

**Big check (every fourth week).** Read the goal from `profile.md` back to them and ask: is this still what you most need, and can you do it better than a month ago? Give one example of something they could not have answered then. If the goal has moved, rewrite the outline from the new goal.

## Plan the week

One theme per week, five new episodes, one review day, and one day for the check-in.

| Day | Morning | Evening |
|---|---|---|
| 1 to 5 | New episode, one idea each | That episode's five cards, plus reviews |
| 6 | Review episode built from the cards missed most | Reviews only |
| 7 | Check-in; next week is made | Nothing new |

Write `plan.md`: for each episode a title, the one idea, the story or real case that carries it, and the five things its cards will ask. Aim for about 70% durable background and 30% current events, with the current events dated, because background is still true next year. Order the week so each episode leans on the one before.

Show the learner the titles with a line each and wait for an OK or edits before writing scripts or making audio. Planning is cheap and audio is not, and this glance is the one point where they steer the content directly. Mark the plan "approved" with the date.

## Make the week

For each of the five days, in this order:

1. **Fact sheet** (`dN-<slug>.facts.md`). Every fact the episode and its cards will use, each with a source link, primary sources first. Mark anything contested with whose view it is.
2. **Fact-check.** A separate pass checks each fact against its source by opening it, not from memory. A fresh subagent is best if you have one, since it has not seen your reasoning. Ask it two extra things: what has happened on this topic recently (your own knowledge stops at your training date, and a listener will notice a missing recent event), and whether each link actually opens. Drop what cannot be confirmed. Record in the sheet how it was checked, and say plainly when no expert has reviewed it. Expect corrections: in the first week this skill was used, about one fact in six needed one.
3. **Cards**, written only from the fact sheet.
4. **Script**, written only from the fact sheet, so the quiz never asks what the episode did not say. Check that every card's answer is said out loud in the episode. Stories pull in extra details as you write; anything in a script or a card's explanation that is not on the fact sheet goes back to step 2 before audio.
5. **Audio.**

Writing both halves from one checked sheet is the heart of this skill: each fact is verified once, and the morning and evening can never disagree.

When all five days are written, put the week's lessons together as `unit.json`, add the unit to `course.json`, and walk the learner through adding it to the app (one upload, under a minute).

### Episode shape

Ten to fifteen minutes is about 1,500 to 2,200 words at a speaking pace of 150 words a minute.

1. **Recall.** One question about yesterday's idea, a pause, then the answer. On day 1, a question from last week.
2. **Story.** A real case, person or moment that shows why the idea exists.
3. **The idea.** Plainly, with one example.
4. **So what.** What it changes about the kind of work the learner does, phrased generally.
5. **Hold these.** Two or three questions to carry to the evening, without answers. They match that evening's cards.

Write for the ear: short sentences, one idea each; say where you are ("first", "now the other side"); no lists, links, brackets or symbols; round numbers and say them the way a person would; name people in full with their role the first time; explain each term in a few words when it first comes up; repeat the main point at the end.

### Getting the episode to their ears

Use the best route this session and this person have, and record it in `profile.md`:

1. **A podcast or text-to-speech skill or tool already in this session.** Use it.
2. **Their own private podcast feed.** If you can run commands on their computer, set this up once with `references/podcast.md`: a free local voice model makes the audio, the files go on a free static host, and the learner follows one feed address in their podcast app. After that, episodes just appear on their phone. `scripts/make_audio.py` and `scripts/build_feed.py` do the work.
3. **No audio tools.** Hand over each script as plain text and have them use a read-aloud app or their phone's screen reader. This is still a paired course.

Title episodes so the order is obvious, for example "W1 D2: The National Emergencies Act". A feed address is unlisted, not private: anyone who has it can listen. So scripts, titles and descriptions must never include what the learner told you about their job or their gaps. Say "you" and keep it general.

### Review day

After day 5's cards, take the five to eight cards the learner missed most that week and build a short episode that explains each one a different way from the first time. No new cards. This needs a session on day 6 and some way to know what they missed; if either is missing, skip it and fold the hard cards into next week's recall questions.

## Things to keep straight

- **Accuracy over coverage.** People will rely on this at work. Leave out what you cannot verify, separate allegation from established fact, and never invent numbers, quotes or dates.
- **Plain language.** Everyday words, short sentences, a concrete example for every idea, in the audio and on the cards.
- **Don't decide for them.** Never drop a topic or a card because they struggled with it. Tell them what you saw and ask.
