# Harry Potter Fanfic Project

Image hosting + prompt files for Harry Potter 21+ Fanfic.

## Structure

```
characters/              Character image folders (35 characters)
  lily_potter/            Images for Lily Potter
  hermione_granger/       Images for Hermione Granger
  ...                     (35 folders total)

prompts/                  Writing prompt files (for AI chat)
  generic_complete_prompt.txt   Generic 21+ writing guide (reusable for any story)
  hp_complete_prompt.txt        HP-specific supplement (characters, canon, outline)
  pronoun_styles.md             11 pronoun styles (A-K) + Mix

README.md                 This file
.gitignore                Git ignore rules
```

## Prompts

### generic_complete_prompt.txt
Generic 21+ novel writing guide. Self-contained. Reusable for ANY 21+ story.
Contains: identity, structure, appearance, vocabulary, pronoun styles, restrictions, checklist.

### hp_complete_prompt.txt
Harry Potter story-specific supplement. Pair with generic prompt.
Contains: 35 characters (with celebrity references), canon events (7 books condensed), story structure, HP-specific restrictions.

### pronoun_styles.md
11 pronoun styles (A-K) + Mix. Each style has 6 sections: main table, self-reference, intimate, context variations, HP examples, banned.

## Character Images

Each character folder contains images named: `<image_key>_<NN>.<ext>`
- `image_key` = celebrity reference (e.g., `iu`, `song_jihyo`)
- `NN` = sequential number (01, 02, 03...)
- Extensions: .jpg, .png, .webp

Example: `characters/hermione_granger/song_jihyo_15.jpg`

## Usage

### For AI chat (DeepSeek, ChatGPT, Claude):
1. Copy `prompts/generic_complete_prompt.txt` content
2. Copy `prompts/hp_complete_prompt.txt` content
3. Paste both into AI chat
4. AI confirms understanding + asks user to choose pronoun style

### For Z.ai agents:
- Image management: `python3 scripts/agents/image_agent.py`
- Story tracking: `python3 scripts/agents/story_agent.py`
- Canon reference: `python3 scripts/agents/canon_agent.py`
- Restriction checking: `python3 scripts/agents/restriction_agent.py`
- Prompt sync: `python3 scripts/agents/prompt_sync_agent.py sync`

## Branch

- `staging` - active development (uploads + edits)
- `main` - stable (merge from staging when ready)

## Notes

- Public repo for image hosting + prompt files only
- No sensitive data stored here
- All images are reference photos for character visualization
- Prompt files are writing guides for 21+ fanfiction

## Config

Project config: `project.json` (not in this repo, local only)
GitHub config: `scripts/github_config.json` (local only)
GitHub PAT: `scripts/.github_token` (local only, never commit)

---
*Last updated: Aug 2, 2026*
