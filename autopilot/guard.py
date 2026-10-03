"""
autopilot/guard.py: safety rails for the scheduled cloud agent (AUTOPILOT.md §3).

Active only when TPG_AUTOPILOT=1 (set in the cloud environment). On the user's own PC nothing changes.

    from autopilot import guard
    guard.stop_if_paused()                       # kill switch: AUTOPILOT_PAUSED in the repo root
    n = guard.allowance("links", wanted=5)       # how many fit under today's cap (6 links, 3 drafts, 0 publishes)
    guard.record("links", 2, target="post 404", detail="IL-7a, IL-7b", undo="python inject_links.py --restore …")
    guard.dfs_check(estimate_usd=0.20)           # stop if the month's DataForSEO spend would pass $5
    guard.dfs_spent(0.18)
    guard.strike("post 404 link not live after upload")   # 2 strikes in 7 days → AUTOPILOT_PAUSED

    python -m autopilot.guard                    # status: paused?, today's counts, month spend, strikes
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAUSE_FILE = ROOT / "AUTOPILOT_PAUSED"
LEDGER = ROOT / "autopilot" / "ledger.json"
DAILY_CAPS = {"links": 6, "drafts": 3, "publishes": 0}
DFS_MONTHLY_USD = 5.00
STRIKES_TO_PAUSE, STRIKE_WINDOW_DAYS = 2, 7
KEEP_ACTIONS_DAYS = 60


def active():
    return os.environ.get("TPG_AUTOPILOT") == "1"


def _now():
    return datetime.now(timezone.utc)


def _today():
    return _now().date().isoformat()


def _month():
    return _now().strftime("%Y-%m")


def load():
    if LEDGER.is_file():
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
    else:
        data = {}
    for key, empty in (("days", {}), ("months", {}), ("actions", []), ("strikes", [])):
        data.setdefault(key, empty)
    return data


def save(data):
    cutoff = (_now() - timedelta(days=KEEP_ACTIONS_DAYS)).isoformat()
    data["actions"] = [a for a in data["actions"] if a["at"] >= cutoff]
    keep_days = {(_now().date() - timedelta(days=i)).isoformat() for i in range(KEEP_ACTIONS_DAYS)}
    data["days"] = {d: v for d, v in data["days"].items() if d in keep_days}
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def paused():
    return PAUSE_FILE.is_file()


def stop_if_paused():
    if active() and paused():
        reason = PAUSE_FILE.read_text(encoding="utf-8").strip() or "no reason given"
        sys.exit(f"PAUSED: AUTOPILOT_PAUSED exists ({reason}). Nothing done. Delete the file to resume.")


def used_today(kind, data=None):
    return (data or load())["days"].get(_today(), {}).get(kind, 0)


def allowance(kind, wanted):
    """How many of `wanted` actions fit under today's cap. Outside autopilot: all of them."""
    if not active():
        return wanted
    stop_if_paused()
    left = max(DAILY_CAPS[kind] - used_today(kind), 0)
    return min(wanted, left)


def record(kind, n, target, detail="", undo=""):
    """Count n actions against today's cap and log them (only under autopilot)."""
    if not active() or n <= 0:
        return
    data = load()
    day = data["days"].setdefault(_today(), {})
    day[kind] = day.get(kind, 0) + n
    data["actions"].append({"at": _now().isoformat(timespec="seconds"), "kind": kind, "n": n,
                            "target": target, "detail": detail, "undo": undo})
    save(data)


def dfs_month_spend(data=None):
    return (data or load())["months"].get(_month(), {}).get("dfs_usd", 0.0)


def dfs_check(estimate_usd):
    """Stop before a paid DataForSEO call that would push the month past the budget."""
    if not active():
        return
    stop_if_paused()
    spent = dfs_month_spend()
    if spent + estimate_usd > DFS_MONTHLY_USD:
        sys.exit(f"BUDGET: DataForSEO spend this month ${spent:.2f} + estimate ${estimate_usd:.2f} "
                 f"would pass ${DFS_MONTHLY_USD:.2f}. Nothing bought.")


def dfs_spent(usd):
    if not active() or usd <= 0:
        return
    data = load()
    month = data["months"].setdefault(_month(), {})
    month["dfs_usd"] = round(month.get("dfs_usd", 0.0) + usd, 4)
    save(data)


def strike(reason):
    """A failed verification. Two within 7 days create AUTOPILOT_PAUSED (Tier B stops until the user removes it)."""
    if not active():
        return False
    data = load()
    data["strikes"].append({"at": _now().isoformat(timespec="seconds"), "reason": reason})
    cutoff = (_now() - timedelta(days=STRIKE_WINDOW_DAYS)).isoformat()
    data["strikes"] = [s for s in data["strikes"] if s["at"] >= cutoff]
    save(data)
    if len(data["strikes"]) >= STRIKES_TO_PAUSE:
        PAUSE_FILE.write_text(f"{_today()}: {len(data['strikes'])} failed verifications in {STRIKE_WINDOW_DAYS} days: "
                              + "; ".join(s["reason"] for s in data["strikes"]) + "\n", encoding="utf-8")
        return True
    return False


def status():
    data = load()
    lines = [f"Autopilot mode: {'ON (TPG_AUTOPILOT=1)' if active() else 'off (local run)'}",
             f"Kill switch: {'PAUSED: ' + PAUSE_FILE.read_text(encoding='utf-8').strip() if paused() else 'not set'}"]
    for kind, cap in DAILY_CAPS.items():
        lines.append(f"Today {kind}: {used_today(kind, data)} of {cap}")
    lines.append(f"DataForSEO this month: ${dfs_month_spend(data):.2f} of ${DFS_MONTHLY_USD:.2f}")
    lines.append(f"Strikes (last {STRIKE_WINDOW_DAYS} days): {len(data['strikes'])}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(status())
