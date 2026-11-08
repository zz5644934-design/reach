"""Anti-ban guard: per-platform min interval, daily cap, jittered delays. State in ~/.reach/state.json."""
import json, random, time
from pathlib import Path

HOME = Path.home() / ".reach"
STATE = HOME / "state.json"
MIN_INTERVAL = 25      # sec between page loads on one platform
DAILY_CAP = 150        # page loads per platform per day
MAX_SCROLLS = 8


def _load():
    try:
        return json.loads(STATE.read_text("utf-8"))
    except Exception:
        return {}


def check_and_wait(platform: str):
    """Sleep until allowed or raise RuntimeError if daily cap hit."""
    st = _load().get(platform, {})
    today = time.strftime("%Y-%m-%d")
    if st.get("day") != today:
        st = {"day": today, "count": 0, "last": st.get("last", 0)}
    if st["count"] >= DAILY_CAP:
        raise RuntimeError(f"daily cap {DAILY_CAP} reached for {platform}; try tomorrow")
    wait = st["last"] + MIN_INTERVAL + random.uniform(0, 10) - time.time()
    if wait > 0:
        time.sleep(wait)
    return st


def record(platform: str, st: dict):
    st["count"] += 1
    st["last"] = time.time()
    data = _load()
    data[platform] = st
    HOME.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(data), "utf-8")


def human_pause(a=1.2, b=3.5):
    time.sleep(random.uniform(a, b))
