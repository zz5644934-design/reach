"""Persistent per-platform Chrome profiles via Playwright. Real installed Chrome, minimal automation fingerprint."""
import random, sys, time
from playwright.sync_api import sync_playwright
from . import limits
from .platforms import PLATFORMS

# Cookie that appears only after a successful login (telegram uses localStorage -> close manually)
AUTH_COOKIES = {"x": "auth_token", "reddit": "reddit_session", "youtube": "SID", "vk": "remixsid",
                "instagram": "sessionid", "tiktok": "sessionid", "facebook": "c_user", "linkedin": "li_at"}

ARGS = ["--disable-blink-features=AutomationControlled"]
LOGIN_HINTS = ("/login", "signin", "sign_in", "accounts/login", "i/flow/login", "checkpoint", "accounts.google.com")
EXIT_NEED_LOGIN = 3
POST_SEL = "article, shreddit-post, ytd-video-renderer, [data-testid='tweet']"


def profile_dir(platform):
    d = limits.HOME / "profiles" / platform
    d.mkdir(parents=True, exist_ok=True)
    return str(d)


def _ctx(p, platform, headless):
    return p.chromium.launch_persistent_context(
        profile_dir(platform), channel="chrome", headless=headless,
        args=ARGS, ignore_default_args=["--enable-automation"],
        viewport={"width": 1366, "height": 850} if headless else None,
        locale="ru-RU")


def login(platform):
    """Open visible Chrome; user logs in manually; session saved when the window is closed."""
    with sync_playwright() as p:
        ctx = _ctx(p, platform, headless=False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(PLATFORMS[platform]["login"])
        cookie = AUTH_COOKIES.get(platform)
        print(f"[{platform}] Log in in the opened window; it closes itself after login.", file=sys.stderr)
        closed = []
        ctx.on("close", lambda *_: closed.append(1))
        try:
            while not closed:
                if cookie and any(c["name"] == cookie for c in ctx.cookies()):
                    time.sleep(4)  # let the session settle/flush
                    ctx.close()
                    print(f"[{platform}] logged in, session saved.", file=sys.stderr)
                    return
                time.sleep(1.5)
        except Exception:
            pass


def read(platform, url, scrolls=2, max_chars=20000):
    scrolls = min(scrolls, limits.MAX_SCROLLS)
    st = limits.check_and_wait(platform)
    with sync_playwright() as p:
        ctx = _ctx(p, platform, headless=True)
        try:
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                # HTTP error response (e.g. X blocks anonymous) -> treat as login needed
                limits.record(platform, st)
                if "ERR_HTTP_RESPONSE_CODE_FAILURE" in str(e):
                    return None, url
                raise
            limits.human_pause(2, 4)
            final = page.url
            if any(h in final.lower() for h in LOGIN_HINTS) and not any(h in url.lower() for h in LOGIN_HINTS):
                limits.record(platform, st)
                return None, final
            # Feeds are virtualized (X, etc.): collect posts after every scroll step, dedupe.
            posts, seen = [], set()

            def collect():
                for t in page.eval_on_selector_all(POST_SEL, "els => els.map(e => e.innerText)"):
                    t = t.strip()
                    if t and t not in seen:
                        seen.add(t)
                        posts.append(t)

            collect()
            for _ in range(scrolls):
                page.mouse.wheel(0, random.randint(500, 900))
                limits.human_pause(1.5, 3.5)
                collect()
            title = page.title()
            text = "\n\n---\n\n".join(posts) if len(posts) >= 2 else page.inner_text("body")
        finally:
            ctx.close()
    limits.record(platform, st)
    return f"# {title}\n{final}\n\n{text}"[:max_chars], final
