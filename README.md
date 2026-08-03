# Harry Potter Fanfic Project

Image hosting + prompt files for Harry Potter 21+ Fanfic.

## After Server Rollback - RESTORE INSTRUCTIONS

If the Z.ai server rolled back and you lost local files:

### Step 1: Download restore script (no PAT needed)

    curl -o /home/z/my-project/hp_project_restore.py https://raw.githubusercontent.com/hungnguyenhoang0103/harry_potter-fanfic-z.ai-images-9ad58zx/staging/hp_project_restore.py

### Step 2: List available backups on GitHub

    python3 /home/z/my-project/hp_project_restore.py list-github

### Step 3: Download + restore (replace TIMESTAMP)

    python3 /home/z/my-project/hp_project_restore.py restore-timestamp TIMESTAMP

### Step 4: Create new GitHub PAT (if needed)

1. Go to https://github.com/settings/personal-access-tokens/new
2. Fine-grained token for this repo, "Contents: Read and write"
3. Save:

    echo "github_pat_xxx" > /home/z/my-project/scripts/.github_token

### Step 5: Verify

    ls /home/z/my-project/download/*.html
    ls /home/z/my-project/scripts/agents/*.py

### Step 6: Create new backup

    python3 /home/z/my-project/scripts/agents/backup_agent.py create

---

## Structure

    hp_project_restore.py     Standalone restore script (survives rollback)
    characters/               Character image folders (35 characters)
    prompts/                  Writing prompt files
      generic_complete_prompt.txt   Generic 21+ writing guide (reusable)
      hp_complete_prompt.txt        HP-specific supplement
      pronoun_styles.md             11 pronoun styles (A-K) + Mix
    README.md                 This file (includes restore instructions)
    .gitignore

## Prompts

- **generic_complete_prompt.txt** - 21+ writing guide, reusable for any story
- **hp_complete_prompt.txt** - HP characters, canon events, story structure
- **pronoun_styles.md** - 11 styles (A-K) + Mix, each with 6 sections

## Character Images

Naming: `<image_key>_<NN>.<ext>`
Example: `characters/hermione_granger/song_jihyo_15.jpg`

## Usage

### AI chat (DeepSeek, ChatGPT, Claude):
1. Copy generic_complete_prompt.txt + hp_complete_prompt.txt
2. Paste into AI chat
3. AI confirms + asks pronoun style

### Z.ai agents:
- Image: `python3 scripts/agents/image_agent.py`
- Story: `python3 scripts/agents/story_agent.py`
- Canon: `python3 scripts/agents/canon_agent.py`
- Restriction: `python3 scripts/agents/restriction_agent.py`
- Backup: `python3 scripts/agents/backup_agent.py create`

## Config (local only)
- project.json
- scripts/github_config.json
- scripts/.github_token

---
Last updated: Aug 2, 2026
