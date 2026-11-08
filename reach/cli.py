import argparse, sys
from . import browser
from .platforms import PLATFORMS, platform_for_url


def main():
    ap = argparse.ArgumentParser(prog="reach", description="Read-only social reader with persistent sessions")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("login"); sp.add_argument("platform", choices=PLATFORMS)
    sp = sub.add_parser("read"); sp.add_argument("url"); sp.add_argument("--scroll", type=int, default=2)
    sp.add_argument("--max-chars", type=int, default=20000)
    sp = sub.add_parser("search"); sp.add_argument("platform", choices=PLATFORMS); sp.add_argument("query")
    sp.add_argument("--scroll", type=int, default=2)
    sp = sub.add_parser("profile"); sp.add_argument("platform", choices=PLATFORMS); sp.add_argument("user")
    sp.add_argument("--scroll", type=int, default=2)
    sub.add_parser("platforms")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if a.cmd == "platforms":
        print("\n".join(PLATFORMS)); return
    if a.cmd == "login":
        browser.login(a.platform); return

    mc = 20000
    if a.cmd == "read":
        plat, url, mc = platform_for_url(a.url), a.url, a.max_chars
        if not plat:
            sys.exit("unknown platform for URL; supported: " + ", ".join(PLATFORMS))
    elif a.cmd == "search":
        plat = a.platform
        f = PLATFORMS[plat]["search"]
        if not f:
            sys.exit(f"search not supported for {plat}; use `reach read <url>`")
        url = f(a.query)
    else:
        plat = a.platform
        url = PLATFORMS[plat]["profile"](a.user)

    try:
        text, final = browser.read(plat, url, a.scroll, mc)
    except RuntimeError as e:
        sys.exit(f"LIMIT: {e}")
    if text is None:
        print(f"NEED_LOGIN: run `reach login {plat}` (redirected to {final})", file=sys.stderr)
        sys.exit(browser.EXIT_NEED_LOGIN)
    print(text)


if __name__ == "__main__":
    main()
