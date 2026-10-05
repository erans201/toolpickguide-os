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


class TestNotifyOwner(unittest.TestCase):
    def test_recipient_is_fixed_and_password_never_printed(self):
        from autopilot import notify_owner
        msg = notify_owner.build("eran@toolpickguide.com", "Daily Digest · OK", "Status: OK", doc="https://docs.google.com/x")
        self.assertEqual(msg["To"], "cezaris.joe@gmail.com")
        self.assertIn("Full report: https://docs.google.com/x", msg.get_content())
        tmp = Path(tempfile.mkdtemp()) / "m.txt"
        tmp.write_text("Status: OK", encoding="utf-8")
        smtp = mock.MagicMock()
        smtp.__enter__.return_value.login.side_effect = Exception("bad login for secret123")
        env = {"BIZ_MAIL_ADDRESS": "eran@toolpickguide.com", "BIZ_MAIL_PASSWORD": "secret123"}
        with mock.patch.dict(os.environ, env), mock.patch.object(notify_owner.smtplib, "SMTP_SSL", return_value=smtp),                 mock.patch.object(sys, "argv", ["x", "--subject", "s", "--file", str(tmp)]):
            with self.assertRaises(SystemExit) as cm:
                notify_owner.main()
        self.assertNotIn("secret123", str(cm.exception))
        self.assertIn("[REDACTED]", str(cm.exception))


class TestInjectLinks(unittest.TestCase):
    def test_affiliate_row_gets_sponsored_rel(self):
        import inject_links
        html = '<!-- wp:paragraph --><p>If outbound is your channel, look at Close.</p><!-- /wp:paragraph -->'
        new, _ = inject_links.insert_link(html, "Close", "https://refer.close.com/abc")
        self.assertIn('<a href="https://refer.close.com/abc" rel="sponsored nofollow noopener" target="_blank">Close</a>', new)
        new2, _ = inject_links.insert_link(html, "outbound", "/crm/")
        self.assertIn('<a href="/crm/">outbound</a>', new2)

    def test_link_present(self):
        import inject_links
        self.assertTrue(inject_links.link_present('<a href="/crm/">x</a>', "/crm/"))
        self.assertTrue(inject_links.link_present('<a href="https://toolpickguide.com/crm/">x</a>', "/crm/"))
        self.assertFalse(inject_links.link_present('<a href="/crm-tools/">x</a>', "/crm/"))


class TestJuniaGate(unittest.TestCase):
    CLEAN = {"claimed_n": 0, "title": "Client Intake Form Template", "question_items": 0, "unknown_amounts": [],
             "banned": [], "tested": [], "long_paragraphs": [], "leftovers": [], "hotlinked_images": [],
             "no_disclosure": False, "faq_sections": 1, "offlist_external": [], "blocked_external": [], "unjudged_external": [], "missing_tools": [],
             "excluded_present": [], "missing_external": []}

    def test_gate(self):
        import junia_draft
        self.assertTrue(junia_draft.gate_clean(self.CLEAN))
        self.assertFalse(junia_draft.gate_clean({**self.CLEAN, "unknown_amounts": ["$99"]}))
        self.assertFalse(junia_draft.gate_clean({**self.CLEAN, "claimed_n": 60, "title": "60 questions", "question_items": 40}))
        self.assertTrue(junia_draft.gate_clean({**self.CLEAN, "offlist_external": ["www.ftc.gov"]}))
        self.assertFalse(junia_draft.gate_clean({**self.CLEAN, "blocked_external": ["spam.example"]}))
        self.assertFalse(junia_draft.gate_clean({**self.CLEAN, "unjudged_external": ["new.example"]}))

    def test_stock_photos_no_longer_block_the_gate(self):
        import junia_draft
        self.assertTrue(junia_draft.gate_clean({**self.CLEAN, "hotlinked_images": ["https://images.unsplash.com/p"]}))

    def test_rehost_swaps_urls_and_skips_non_images(self):
        import junia_draft
        src = "https://images.unsplash.com/photo-1?w=1200&amp;q=80"
        raw = f'<img src="{src}"/><img src="https://evil.example/x.html"/><img src="http://plain.example/a.jpg"/>'
        def fake_get(url, timeout):
            ctype = "image/jpeg" if "unsplash" in url else "text/html"
            return mock.Mock(content=b"x", headers={"Content-Type": ctype}, raise_for_status=lambda: None)
        upload = mock.Mock(return_value=77)
        wp = mock.Mock(return_value={"source_url": "https://toolpickguide.com/wp-content/uploads/a.jpg"})
        with mock.patch("requests.get", side_effect=fake_get),                 mock.patch.object(junia_draft, "BACKUP_DIR", Path(tempfile.mkdtemp())):
            out, ids = junia_draft.rehost_images(None, raw, [src, "https://evil.example/x.html", "http://plain.example/a.jpg"],
                                                 "alt", "slug", upload, wp)
        self.assertEqual(ids, [77])
        self.assertIn('src="https://toolpickguide.com/wp-content/uploads/a.jpg"', out)
        self.assertNotIn("unsplash", out)
        self.assertIn("evil.example", out)  # not an image: left alone
        upload.assert_called_once()

    def test_junia_own_links_are_judged_per_domain(self):
        import junia_draft
        brief = {"external": ["https://www.honeybook.com/pricing"]}
        links = ["https://www.honeybook.com/pricing", "https://www.ftc.gov/x", "https://blog.spam.example/y",
                 "https://new-site.example/z"]
        got = junia_draft.judge_offlist(links, brief, {"ftc.gov": "trusted", "spam.example": "blocked"})
        self.assertEqual(got, {"blocked_external": ["blog.spam.example"], "unjudged_external": ["new-site.example"]})


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
