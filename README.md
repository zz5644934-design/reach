# reach

A Claude Code plugin that lets Claude read social networks through **your own logged-in sessions**: X, Reddit, YouTube, VK, Telegram (web), Instagram, TikTok, Facebook, LinkedIn.

You log in once in a real Chrome window. The session is stored locally in `~/.reach/profiles/<platform>`. Claude then uses it to search and read pages for research. Read-only: it never posts, likes, follows or messages.

No API keys, no cookies pasted anywhere, nothing leaves your machine except normal browser traffic to the site itself.

## Install

Requires Python 3.10+ and Google Chrome.

```bash
pip install git+https://github.com/zz5644934-design/reach
```

Then in Claude Code:

```
/plugin marketplace add zz5644934-design/reach
/plugin install reach@reach
```

## Use

Log in once per platform (a Chrome window opens, the window closes itself after login):

```bash
reach login x
```

Then just ask Claude, e.g. "research what people say about X on Reddit and X". Under the hood it runs:

```bash
reach search x "query"
reach profile reddit username
reach read https://...
```

If a session expired, the CLI exits with `NEED_LOGIN` and Claude asks you to run `reach login <platform>` again.

## Ban-risk mitigation

- Real installed Chrome, no automation flag
- At least 25 s (plus random jitter) between page loads per platform
- Cap of 150 page loads per platform per day, max 8 scrolls per page
- Sequential only, read-only
- Use a separate account on aggressive platforms (X, Instagram, TikTok). The risk is reduced, not zero.

## Privacy

Browser profiles and rate-limit state live in `~/.reach`. Nothing is sent anywhere else. Delete the folder to log out everywhere.
