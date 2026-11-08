---
name: reach
description: Read social media pages (X, Reddit, YouTube, VK, Telegram, Instagram, TikTok, Facebook, LinkedIn) via the `reach` CLI using the user's saved logged-in sessions. Use when the user asks to look at, search, or summarize content from a social network.
---

# reach

Read-only CLI. Never posts, likes, follows or messages.

Commands:
- `reach read <url> [--scroll N]` - page text
- `reach search <platform> "<query>"`
- `reach profile <platform> <user>`
- `reach login <platform>` - user only, opens a visible Chrome window

Research workflow (when the user asks to research a topic/person/trend):
1. Pick 2-4 relevant platforms; run `reach search` on each with 1-2 focused queries (different phrasings).
2. From results, open only the 3-6 most relevant posts/profiles with `reach read` (`--scroll 2-3` for comments).
3. Run calls one by one, never in parallel; don't retry a failed load repeatedly.
4. Report: key findings, who said it, links, and what you could not access (NEED_LOGIN/LIMIT). Mark claims from social posts as unverified.

Rules:
- Exit code 3 / `NEED_LOGIN`: tell the user to run `reach login <platform>`, log in manually, close the window. Never ask for or type passwords.
- `LIMIT:` means the anti-ban daily cap is hit. Stop, do not work around it.
- Calls are deliberately slow (>=25s between loads per platform). Fetch few, relevant pages; no loops over many URLs; no parallel calls.
- Prefer `--scroll 1-3`. Summarize results for the user; don't dump raw page text.
