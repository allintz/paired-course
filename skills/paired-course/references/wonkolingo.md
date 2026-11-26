# Adding a custom course to WonkoLingo

For an AI assistant that has been asked to make quiz cards for a learner's own course in WonkoLingo (https://wonkolingo.com). WonkoLingo is a spaced-repetition quiz app, on the web and the iPhone App Store. Anyone signed in can add their own course as a single JSON file. You write the file; the learner adds it in the app. There is no way for you to load it for them.

## 1. Read the course guide first

The full format, with every field, limit and question type, is at:

- https://wonkolingo.com/course-guide.md (the rules)
- https://wonkolingo.com/example-course.json (a small complete course)

Fetch the guide as raw text and read all of it before writing a card. A summarizing web tool can drop table rows and exact limits, and the app rejects files that break them. If anything in this file disagrees with the guide, the guide wins.

## 2. The shape of a paired course

One personal course per learner, growing by one unit a week:

- **Course `id`:** distinctive, lowercase letters, numbers and hyphens, 2 to 40 characters, for example `sam-energy-policy`. It never changes; uploading a file with the same `id` replaces the learner's earlier version.
- **One unit per week**, titled with the week's theme.
- **One lesson per episode**, with the same title as the episode.
- **Five questions per lesson.** WonkoLingo serves five new cards a day per course by default, so five cards means each evening gets exactly that morning's lesson.
- **Limits:** at most 12 units, 8 lessons per unit, 400 questions and 200 KB per course. After twelve weeks, start a second course (`sam-energy-policy-2`).

Every question needs a permanent `id` that describes it (`sunset-clause-purpose`, never `q1` or `w2d3-1`). The learner's review history hangs on that id. Keep it when you fix the wording; never reuse it for a different question.

## 3. Writing the cards

The guide's writing rules matter more than its format rules. The ones that decide whether a card is any good:

- **Only ask what the episode said.** Write cards from the same checked fact sheet as the script.
- **Every card works for someone who missed the episode.** The app cannot tell whether they listened. Test each card by imagining a learner who skipped that morning: the question must give enough context to make a fair guess from the options, and the explanation `x` must teach the idea in full, with the example, so they have learned it by the time the card comes back. Never test a detail that only the episode's story supplied (a name, a date, an anecdote) unless the explanation tells that story too.
- **Plain words.** Short sentences, no jargon unless the term is the point of the card.
- **A concrete example on every card:** a real law, case, company or event, usually in the explanation `x`.
- **One idea per card.** Split anything that asks two things.
- **Every card stands on its own.** It will come back weeks later, out of order. Never write "this episode", "as we heard" or "this week"; put the needed context in the question.
- **The right answer is short and complete:** 3 to 10 words that make sense with no options shown.
- **Wrong options a smart beginner might believe:** a near miss, a rival's real argument, a related idea that answers a different question. Give each a one-line `ow` saying why it is wrong. If you can't, it is too close to right.
- **The right option is never the longest** or the only careful-sounding one.
- **No "best" or "most" questions when several answers are true.**
- **Spell out acronyms** the first time on each card.
- Mostly multiple choice (`mc`), about one short-answer card (`recall`, always with a `choice` version) per lesson, and the odd matching or ordering card.
- Say in the course `caveat` what date the facts are current as of and how they were checked.

## 4. Week one: the whole course file

```json
{
  "format": "wonkolingo-course/1",
  "id": "sam-energy-policy",
  "title": "Sam: Energy Policy",
  "description": "Cards paired with a daily podcast on how US energy permitting works.",
  "level": "intermediate",
  "categories": ["policy"],
  "caveat": "Facts current as of <month year>. Checked by AI against the linked sources, not by an expert.",
  "units": [
    {
      "title": "Week 1: Who permits what",
      "desc": "The agencies and laws behind a federal permit.",
      "lessons": [
        {
          "title": "The National Environmental Policy Act",
          "items": [
            {
              "id": "nepa-what-it-requires",
              "t": "mc",
              "p": "What does the National Environmental Policy Act (NEPA) require a federal agency to do before a major project?",
              "o": ["Study and disclose the environmental effects", "Prove the project will cause no environmental harm", "Win a vote of approval from Congress beforehand", "Hold a referendum in each state it crosses"],
              "a": 0,
              "ow": ["", "NEPA requires a study, not a clean result. An agency can approve a harmful project.", "Congress has no project-by-project vote under NEPA.", "NEPA is federal and has no referendum step."],
              "keys": ["study and disclose environmental effects"],
              "x": "NEPA (1970) is a look-before-you-leap law. For example, a new interstate highway needs an environmental impact statement, but the law does not say what the agency must decide after reading it."
            }
          ]
        }
      ]
    }
  ]
}
```

(One question shown; a real lesson has five.) Check the file against the "Before you hand over the file" list at the end of the guide.

Then tell the learner, in these words or close to them:

1. Open WonkoLingo and sign in.
2. Go to **Courses** and choose **+ Make one**.
3. Upload the file, or paste its contents into the box.
4. If the app lists problems, send them to me. (They look like `units[0].lessons[1].items[2].a: ...`. Fix exactly those and give a new file.)
5. Check the course is in your daily mix at 5 new cards a day.

If you can't create files, give the whole course in one code block for them to paste.

## 5. Every later week: only the new unit

Do not send the whole course again. Give a small file with just the new week:

```json
{ "units": [ { "title": "Week 2: Transmission lines", "desc": "...", "lessons": [ ...five lessons... ] } ] }
```

The learner opens the course's page in the app, chooses **Add questions**, and uploads or pastes it. The new unit goes at the end. Also add the unit to your own full copy of the course (`course.json`), so you always know every `id` already used and can rebuild the course if needed.

To fix one card, send `{ "items": [ { ...the corrected question with its existing id... } ] }` through **Add questions**. A question with the `id` of one already in the course replaces it.

## 6. If the app already has a course on the topic

WonkoLingo has built-in courses, mostly on AI policy, Congress and US democracy. If one fits a week's theme, the learner can switch it on in their daily mix and you write episodes that follow its lessons, with no new cards. Only do this if you can see the cards themselves; an episode has to teach every card in its lesson.
