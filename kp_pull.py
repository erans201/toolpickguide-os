"""
kp_pull.py: pull keyword ideas from Google Keyword Planner via the Google Ads API (read-only), then run kp_ingest.py.

Setup (once; see the steps in data/README.md → "Keyword Planner API"):
  - Google Ads manager account with an approved developer token (API Center)
  - Google Cloud (same project): Google Ads API enabled + OAuth client (Desktop app) saved as ads-oauth-client.json
  - pip install google-ads google-auth-oauthlib

    python kp_pull.py --auth       # one time: browser sign-in → writes google-ads.yaml + kp-config.json
    python kp_pull.py --check      # confirm access to your Ads account
    python kp_pull.py              # all 6 seed groups from data/README.md → data/kp-api-<date>-g<n>.csv → kp_ingest
    python kp_pull.py --group 2    # one seed group only

Secrets: google-ads.yaml (developer token + refresh token) and ads-oauth-client.json. Never print, copy, or commit them.
Only the user runs this script. It only reads keyword ideas: no campaigns, no spend.
"""

import argparse
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

DATA = Path("data")
YAML = Path("google-ads.yaml")
OAUTH_CLIENT = Path("ads-oauth-client.json")
CONFIG = Path("kp-config.json")  # non-secret: which Ads account to query
SCOPE = ["https://www.googleapis.com/auth/adwords"]
US, ENGLISH = "2840", "1000"


def digits(text):
    return re.sub(r"\D", "", text or "")


def seed_groups():
    """Seed groups from the table in data/README.md: | # | Cluster | seeds, comma, separated |"""
    groups = {}
    for line in (DATA / "README.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", line)
        if m:
            groups[int(m.group(1))] = (m.group(2), [s.strip() for s in m.group(3).split(",") if s.strip()][:20])
    if not groups:
        sys.exit("ERROR: no seed groups found in data/README.md")
    return groups


def auth():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        sys.exit("ERROR: run  pip install google-ads google-auth-oauthlib")
    if not OAUTH_CLIENT.is_file():
        sys.exit(f"ERROR: {OAUTH_CLIENT} not found. Download the OAuth client (Desktop app) JSON and save it under that name.")
    token = input("Developer token (Ads manager account → Admin → API Center): ").strip()
    mcc = digits(input("Manager account ID (e.g. 123-456-7890): "))
    cid = digits(input("Ads account ID that has Keyword Planner (e.g. 987-654-3210): "))
    if not (token and len(mcc) == 10 and len(cid) == 10):
        sys.exit("ERROR: developer token and two 10-digit account IDs are required.")
    print("A browser window opens: sign in with the Google account that owns the Ads accounts.")
    creds = InstalledAppFlow.from_client_secrets_file(str(OAUTH_CLIENT), SCOPE).run_local_server(port=0)
    client = json.loads(OAUTH_CLIENT.read_text(encoding="utf-8"))
    client = client.get("installed") or client.get("web") or {}
    YAML.write_text("\n".join([
        f"developer_token: {token}", f"client_id: {client['client_id']}", f"client_secret: {client['client_secret']}",
        f"refresh_token: {creds.refresh_token}", f"login_customer_id: {mcc}", "use_proto_plus: True", ""]), encoding="utf-8")
    CONFIG.write_text(json.dumps({"customer_id": cid}, indent=2), encoding="utf-8")
    print(f"✅ Saved {YAML} (secret) and {CONFIG}. Next: python kp_pull.py --check")


def ads_client():
    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ImportError:
        sys.exit("ERROR: run  pip install google-ads google-auth-oauthlib")
    if not YAML.is_file() or not CONFIG.is_file():
        sys.exit("ERROR: not set up yet. Run: python kp_pull.py --auth")
    return GoogleAdsClient.load_from_storage(str(YAML)), json.loads(CONFIG.read_text(encoding="utf-8"))["customer_id"]


def explain(ex):
    msgs = [e.message for e in ex.failure.errors]
    text = " | ".join(msgs)[:400]
    if "DEVELOPER_TOKEN" in str(ex.failure) or "developer token" in text.lower():
        text += ("\n→ The developer token is not approved for real accounts yet. Wait for the Basic access approval "
                 "email (API Center), or use the manual export in data/README.md meanwhile.")
    return text


def build_request(client, cid, seeds):
    req = client.get_type("GenerateKeywordIdeasRequest")
    req.customer_id = cid
    req.language = client.get_service("GoogleAdsService").language_constant_path(ENGLISH)
    req.geo_target_constants.append(client.get_service("GeoTargetConstantService").geo_target_constant_path(US))
    req.include_adult_keywords = False
    req.keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
    req.keyword_seed.keywords.extend(seeds)
    return req


def money(micros):
    return f"{micros / 1e6:.2f}" if micros else ""


def pull(client, cid, groups):
    from google.ads.googleads.errors import GoogleAdsException
    svc = client.get_service("KeywordPlanIdeaService")
    stamp, files = date.today().isoformat(), []
    for n, (name, seeds) in groups.items():
        try:
            ideas = list(svc.generate_keyword_ideas(request=build_request(client, cid, seeds)))
        except GoogleAdsException as ex:
            sys.exit(f"ERROR (group {n}): {explain(ex)}")
        path = DATA / f"kp-api-{stamp}-g{n}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Keyword", "Avg. monthly searches", "Competition", "Competition (indexed value)",
                        "Top of page bid (low range)", "Top of page bid (high range)"])
            for i in ideas:
                m = i.keyword_idea_metrics
                w.writerow([i.text, m.avg_monthly_searches, m.competition.name.title().replace("Unspecified", ""),
                            m.competition_index, money(m.low_top_of_page_bid_micros), money(m.high_top_of_page_bid_micros)])
        files.append(path)
        print(f"   group {n} · {name}: {len(ideas):,} ideas → {path}")
    return files


def main():
    ap = argparse.ArgumentParser(description="Keyword Planner via Google Ads API (read-only).")
    ap.add_argument("--auth", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--group", type=int)
    a = ap.parse_args()
    if a.auth:
        return auth()

    client, cid = ads_client()
    if a.check:
        from google.ads.googleads.errors import GoogleAdsException
        try:
            rows = client.get_service("GoogleAdsService").search(
                customer_id=cid, query="SELECT customer.id, customer.descriptive_name FROM customer LIMIT 1")
            for r in rows:
                print(f"✅ Access OK: Ads account {r.customer.id} ({r.customer.descriptive_name})")
        except GoogleAdsException as ex:
            sys.exit(f"ERROR: {explain(ex)}")
        return

    groups = seed_groups()
    if a.group:
        groups = {a.group: groups[a.group]}
    DATA.mkdir(exist_ok=True)
    print(f"Keyword Planner · United States · English · {len(groups)} seed group(s)")
    files = pull(client, cid, groups)
    import kp_ingest
    sys.argv = ["kp_ingest.py"] + [str(p) for p in files]
    kp_ingest.main()


if __name__ == "__main__":
    main()
