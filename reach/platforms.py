"""Platform registry: domain, login url, search/profile URL builders."""
from urllib.parse import quote, urlparse

PLATFORMS = {
    "telegram": dict(login="https://web.telegram.org/a/", domains=["web.telegram.org", "t.me"],
                     search=None, profile=lambda u: f"https://t.me/s/{u.lstrip('@')}"),
    "x": dict(login="https://x.com/login", domains=["x.com", "twitter.com"],
              search=lambda q: f"https://x.com/search?q={quote(q)}&f=live",
              profile=lambda u: f"https://x.com/{u.lstrip('@')}"),
    "reddit": dict(login="https://www.reddit.com/login", domains=["reddit.com"],
                   search=lambda q: f"https://www.reddit.com/search/?q={quote(q)}",
                   profile=lambda u: f"https://www.reddit.com/user/{u.removeprefix('u/')}"),
    "youtube": dict(login="https://accounts.google.com/ServiceLogin?service=youtube", domains=["youtube.com", "youtu.be"],
                    search=lambda q: f"https://www.youtube.com/results?search_query={quote(q)}",
                    profile=lambda u: f"https://www.youtube.com/@{u.lstrip('@')}"),
    "vk": dict(login="https://vk.com/login", domains=["vk.com", "vk.ru"],
               search=lambda q: f"https://vk.com/search?c%5Bq%5D={quote(q)}",
               profile=lambda u: f"https://vk.com/{u}"),
    "instagram": dict(login="https://www.instagram.com/accounts/login/", domains=["instagram.com"],
                      search=None, profile=lambda u: f"https://www.instagram.com/{u.lstrip('@')}/"),
    "tiktok": dict(login="https://www.tiktok.com/login", domains=["tiktok.com"],
                   search=lambda q: f"https://www.tiktok.com/search?q={quote(q)}",
                   profile=lambda u: f"https://www.tiktok.com/@{u.lstrip('@')}"),
    "facebook": dict(login="https://www.facebook.com/login", domains=["facebook.com"],
                     search=lambda q: f"https://www.facebook.com/search/top?q={quote(q)}",
                     profile=lambda u: f"https://www.facebook.com/{u}"),
    "linkedin": dict(login="https://www.linkedin.com/login", domains=["linkedin.com"],
                     search=lambda q: f"https://www.linkedin.com/search/results/content/?keywords={quote(q)}",
                     profile=lambda u: f"https://www.linkedin.com/in/{u}"),
}


def platform_for_url(url: str):
    host = (urlparse(url).hostname or "").lower()
    for name, p in PLATFORMS.items():
        if any(host == d or host.endswith("." + d) for d in p["domains"]):
            return name
    return None
