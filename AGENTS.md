# For AI assistants working in this repo

This repo is public. It holds one skill, `skills/paired-course/`, that other people run with their own assistant. Start with `README.md`, then `skills/paired-course/SKILL.md`.

- Keep everything under `skills/` generic: no personal names, no paths or tools from one person's computer, nothing private.
- `learners/` and `owner/` are in `.gitignore` and must never be committed. They hold one person's private notes.
- Commit with the repo's configured no-reply email. Do not change the git identity.
- The skill points at live pages on wonkolingo.com (`/plan-guide.md`, `/course-guide.md`, `/library/`). If you change what the skill says about them, check the pages still say the same.
- The scripts in `skills/paired-course/scripts/` are meant to run on someone else's machine. Test a change with a fresh install (`KOKORO_DIR=<temp folder> ./setup_audio.sh`) before pushing.
