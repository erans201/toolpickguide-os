# New project starter message (template)

How to use:
1. Create a new folder for the project (e.g. `C:\Users\User\Documents\<project-name>`).
2. In the Claude app, start a new Code session in that folder and switch to **Plan mode**.
3. Copy everything between the two lines below, fill in the [brackets], and send it as the first message.

----- copy from here -----

This folder is a new project: [what the agent does, for whom, and the goal; a rough description is fine].

Before any work, set up the project's "second brain". Create only the files that fit this project:

| File | Purpose | Needed |
|---|---|---|
| CLAUDE.md | rules, security, decisions; points to all the others | always |
| MANDATE.md | agent roles and their limits | if more than one role |
| MEMORY.md | research and findings log | if the project involves research |
| LOOP.md | current state at the top + a dated log line for every action and decision | always |
| TASKS.md | numbered tasks with exact steps and who does each one (you or me) | always |
| summary/ | max 10 one-page overviews + a simple one-page diagram of the project | once there's enough content |
| .claude/skills/ | repeatable commands for tasks we do often | later, when needed |

CLAUDE.md must:
- tell every new chat to read MANDATE.md, MEMORY.md, LOOP.md and TASKS.md first;
- list what you may do alone, what needs my OK, and what you must never do;
- include security rules: never read, print or commit passwords, keys or `.env` files; never enter passwords or payment details for me;
- keep a dated list of my decisions.

Working rules:
- Write every decision into these files right away. A new chat only knows what's in them.
- Explain things to me step by step, with exact clicks and no jargon.
- Ask me before inventing business details, prices, legal terms or numbers.
- Never delete or overwrite files without my OK.

Interview me first: ask me the questions you need to fill these files (goal, audience, accounts and tools, what you may do alone, budget, schedule). Then show me the plan for the files before writing them.

----- copy to here -----
