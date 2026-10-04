"""
Offline tests for the autopilot safety rails and cloud-ready tools. No network, no real ledger, no WordPress.

    python -m unittest discover -s tests -v
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from autopilot import guard, healthcheck  # noqa: E402


class GuardCase(unittest.TestCase):
    """Points the guard at a throw-away ledger and kill-switch file."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.patches = [mock.patch.object(guard, "LEDGER", self.tmp / "ledger.json"),
                        mock.patch.object(guard, "PAUSE_FILE", self.tmp / "AUTOPILOT_PAUSED")]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()

    def autopilot(self, on=True):
        return mock.patch.dict(os.environ, {"TPG_AUTOPILOT": "1" if on else "0"})


class TestGuard(GuardCase):
    def test_local_runs_are_untouched(self):
        with self.autopilot(False):
            self.assertEqual(guard.allowance("links", 50), 50)
            guard.record("links", 5, target="post 1")
            guard.dfs_check(99.0)  # no exit outside autopilot
            (self.tmp / "AUTOPILOT_PAUSED").write_text("x")
            guard.stop_if_paused()  # kill switch only binds the autopilot
        self.assertFalse((self.tmp / "ledger.json").exists())

    def test_daily_link_cap(self):
        with self.autopilot():
            self.assertEqual(guard.allowance("links", 10), 6)
            guard.record("links", 4, target="post 1", undo="restore a")
            self.assertEqual(guard.allowance("links", 10), 2)
            guard.record("links", 2, target="post 2")
            self.assertEqual(guard.allowance("links", 10), 0)
        data = json.loads((self.tmp / "ledger.json").read_text())
        self.assertEqual(len(data["actions"]), 2)
        self.assertEqual(data["actions"][0]["undo"], "restore a")

    def test_draft_cap_and_zero_publishes(self):
        with self.autopilot():
            guard.record("drafts", 3, target="draft 9")
            self.assertEqual(guard.allowance("drafts", 1), 0)
            self.assertEqual(guard.allowance("publishes", 1), 0)

    def test_kill_switch(self):
        (self.tmp / "AUTOPILOT_PAUSED").write_text("user stop")
        with self.autopilot(), self.assertRaises(SystemExit) as cm:
            guard.allowance("links", 1)
        self.assertIn("user stop", str(cm.exception))

    def test_dfs_budget(self):
        with self.autopilot():
            guard.dfs_spent(4.50)
            guard.dfs_check(0.40)  # 4.90 fits
            with self.assertRaises(SystemExit):
                guard.dfs_check(0.60)  # 5.10 does not
            guard.dfs_spent(0.25)
            self.assertAlmostEqual(guard.dfs_month_spend(), 4.75)

    def test_two_strikes_pause(self):
        with self.autopilot():
            self.assertFalse(guard.strike("first"))
            self.assertFalse((self.tmp / "AUTOPILOT_PAUSED").exists())
            self.assertTrue(guard.strike("second"))
        self.assertIn("first; second", (self.tmp / "AUTOPILOT_PAUSED").read_text())


class TestInjectLinks(unittest.TestCase):
    def test_link_present(self):
        import inject_links
        self.assertTrue(inject_links.link_present('<a href="/crm/">x</a>', "/crm/"))
        self.assertTrue(inject_links.link_present('<a href="https://toolpickguide.com/crm/">x</a>', "/crm/"))
        self.assertFalse(inject_links.link_present('<a href="/crm-tools/">x</a>', "/crm/"))


class TestJuniaGate(unittest.TestCase):
    CLEAN = {"claimed_n": 0, "title": "Client Intake Form Template", "question_items": 0, "unknown_amounts": [],
             "banned": [], "tested": [], "long_paragraphs": [], "leftovers": [], "hotlinked_images": [],
             "offlist_external": [], "missing_tools": [], "excluded_present": [], "missing_external": []}

    def test_gate(self):
        import junia_draft
        self.assertTrue(junia_draft.gate_clean(self.CLEAN))
        self.assertFalse(junia_draft.gate_clean({**self.CLEAN, "unknown_amounts": ["$99"]}))
        self.assertFalse(junia_draft.gate_clean({**self.CLEAN, "claimed_n": 60, "title": "60 questions", "question_items": 40}))


class TestHealthcheck(unittest.TestCase):
    def test_robots_compare(self):
        tmp = Path(tempfile.mkdtemp()) / "baseline.json"
        tmp.write_text(json.dumps({"robots": {"https://a/": "index, follow", "https://b/": "index, follow",
                                              "https://gone/": "index, follow"}}))
        alerts, notes = [], []
        with mock.patch.object(healthcheck, "BASELINE", tmp):
            healthcheck.compare_robots({"https://a/": "index, follow", "https://b/": "noindex, follow",
                                        "https://new/": "index, follow"}, alerts, notes)
        self.assertEqual(len(alerts), 1)
        self.assertIn("https://b/", alerts[0])
        self.assertTrue(any("new/" in n for n in notes) and any("gone/" in n for n in notes))


class TestPagespeed(unittest.TestCase):
    def test_measure_parses_lab_and_field(self):
        import pagespeed_pull
        body = {"lighthouseResult": {"categories": {"performance": {"score": 0.72}}, "audits": {
                    "largest-contentful-paint": {"numericValue": 3100}, "cumulative-layout-shift": {"numericValue": 0.02},
                    "total-blocking-time": {"numericValue": 150}}},
                "loadingExperience": {"overall_category": "AVERAGE", "metrics": {
                    "LARGEST_CONTENTFUL_PAINT_MS": {"percentile": 2400}, "INTERACTION_TO_NEXT_PAINT": {"percentile": 180},
                    "CUMULATIVE_LAYOUT_SHIFT_SCORE": {"percentile": 5}}}}
        resp = mock.Mock(status_code=200, json=lambda: body, headers={"content-type": "application/json"})
        with mock.patch.object(pagespeed_pull.requests, "get", return_value=resp):
            row = pagespeed_pull.measure("https://toolpickguide.com/", "k")
        self.assertEqual(row["perf_score"], 72)
        self.assertEqual(row["lab_lcp_s"], 3.1)
        self.assertEqual(row["field_inp_ms"], 180)
        self.assertEqual(row["field_cls"], 0.05)
        self.assertEqual(row["verdict"], "fix LCP")


class TestCloudKey(unittest.TestCase):
    """GSC_KEY_JSON is used only when there is no key file (fake key, never a real one)."""
    FAKE = json.dumps({"type": "service_account", "client_email": "x@y.iam.gserviceaccount.com"})

    def test_gsc_uses_env_key(self):
        import gsc_pull
        env = {"GSC_KEY_JSON": self.FAKE, "GSC_KEY_FILE": "does-not-exist.json"}
        with mock.patch.dict(os.environ, env), \
                mock.patch("google.oauth2.service_account.Credentials.from_service_account_info") as info, \
                mock.patch("googleapiclient.discovery.build"):
            gsc_pull.service()
        self.assertEqual(info.call_args[0][0]["client_email"], "x@y.iam.gserviceaccount.com")

    def test_ga_uses_env_key(self):
        import ga_pull
        env = {"GSC_KEY_JSON": self.FAKE, "GSC_KEY_FILE": "does-not-exist.json"}
        with mock.patch.dict(os.environ, env), mock.patch(
                "google.analytics.data_v1beta.BetaAnalyticsDataClient.from_service_account_info") as info:
            ga_pull.client()
        info.assert_called_once()


class TestMailTool(unittest.TestCase):
    def test_only_affiliate_senders_are_shown(self):
        import mail_tool
        doms = ["honeybook.com", "lawmatics.com"]
        self.assertTrue(mail_tool.sender_allowed("HoneyBook <affiliates@honeybook.com>", doms))
        self.assertTrue(mail_tool.sender_allowed("x@mail.lawmatics.com", doms))
        self.assertFalse(mail_tool.sender_allowed("Bank <alerts@mybank.com>", doms))
        self.assertFalse(mail_tool.sender_allowed("evil@honeybook.com.attacker.net", doms))

    def test_draft_needs_exactly_one_recipient(self):
        import mail_tool
        tmp = Path(tempfile.mkdtemp())
        ok = tmp / "ok.md"
        ok.write_text("To: partners@clio.com\nSubject: Hello\n\nBody line.\n", encoding="utf-8")
        self.assertEqual(mail_tool.parse_draft(ok)[0], "partners@clio.com")
        two = tmp / "two.md"
        two.write_text("To: a@x.com, b@y.com\nSubject: Hi\n\nBody\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            mail_tool.parse_draft(two)

    def test_refuses_cloud_autopilot(self):
        import mail_tool
        with mock.patch.dict(os.environ, {"TPG_AUTOPILOT": "1"}), mock.patch.object(sys, "argv", ["mail_tool.py", "--inbox"]):
            with self.assertRaises(SystemExit):
                mail_tool.main()


if __name__ == "__main__":
    unittest.main()
