# Building a course with a lead and workers

Use Claude Fable 5.2 (`claude-fable-5-2`), or a newer Fable model available in the current tool, as the lead. Use Claude Opus 5.5 (`claude-opus-5-5`) for the workers. The lead owns the learner conversation, the course structure, the factual review and the final result.

In Claude Code, start a session with the Fable family alias and pin the worker model for the session:

```bash
CLAUDE_CODE_SUBAGENT_MODEL=claude-opus-5-5 claude --model fable
```

Invoke `paired-course` in that session. Use general-purpose Agent workers with the configured default. In an existing Fable session without the variable, select the `opus` worker model if it resolves to Opus 5.5, or specify the full ID in a Claude Code subagent definition. Check the actual models before claiming this setup was used. If the runtime lacks these models or delegation, name the fallback and keep the evidence review independent of the draft where possible. Model setup references are the [Claude model list](https://platform.claude.com/docs/en/models/overview) and [Claude Code subagent settings](https://code.claude.com/docs/en/sub-agents#choose-a-model).

## Divide the work

1. The lead interviews the learner, checks for relevant library material, and makes the outline and episode sketches. It resolves prerequisites and repeated topics before work is assigned. Keep the learner's existing approval step for the sketches.
2. The lead gives each independent episode or unit to one Opus worker. For a normal five-day week, assign one worker per new episode and run independent assignments in parallel within the available limits. Give each worker its scope, adjacent episode summaries, matching library card ids, and file paths it owns. Share a brief of the learning goal and level. Leave out personal interview details and credentials. Workers return drafts to the lead.
3. Workers produce fact sheets with source links and the supporting passage for each claim. The lead opens the sources and approves, corrects, or drops the claims. It checks dates, contested claims and whether newer events change the story. A separate Opus worker can check a disputed claim if needed. The lead reconciles the evidence and decides what to keep.
4. Workers use the checked sheets to write the cards and scripts for their assignments. The lead checks that the audio teaches every selected card, each card works on its own, the days build on each other, and no fact was introduced without evidence. It sends unclear parts back to the assigned worker for revision and assembles the approved files. The lead handles the final upload instructions and any authorized publishing.
