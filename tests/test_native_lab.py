from __future__ import annotations

import unittest

from urivision.native_profiles import REQUIRED_FAMILIES, coverage_summary, get_native_target, list_native_targets
from urivision.method_router import INTENT_METHODS, route_intent, route_matrix


class NativeLabTests(unittest.TestCase):
    def test_required_families_are_covered(self):
        summary = coverage_summary()
        self.assertGreaterEqual(summary["target_count"], 14)
        self.assertEqual(summary["missing_required_families"], [])
        for fam in REQUIRED_FAMILIES:
            self.assertIn(fam, summary["families"])

    def test_each_profile_has_evidence_and_probes(self):
        for profile in list_native_targets():
            with self.subTest(profile=profile.id):
                self.assertTrue(profile.primary_adapters)
                self.assertTrue(profile.required_probes)
                self.assertTrue(profile.evidence_required)
                self.assertTrue(profile.risk_focus)
                self.assertIn("runtime://local/health/query/check", profile.must_pass_uris)

    def test_method_router_selects_route_for_key_intents(self):
        examples = [
            ("windows-11-uia", "type_text"),
            ("macos-26-ax-apple-silicon", "type_text"),
            ("ubuntu-24-04-wayland", "find_element"),
            ("android-adb-uiautomator", "type_text"),
            ("ios-xcuitest", "press_element"),
            ("hid-kvm-rp2040", "capture_screen"),
        ]
        for profile, intent in examples:
            with self.subTest(profile=profile, intent=intent):
                p = get_native_target(profile)
                decision = route_intent(intent, profile)
                self.assertIsNotNone(decision.selected)
                self.assertIn(decision.selected["adapter"], set(p.primary_adapters) | set(p.fallback_adapters))
                self.assertTrue(decision.selected["available_in_profile"])

    def test_route_matrix_has_all_profiles_and_intents(self):
        matrix = route_matrix()
        targets = {p.id for p in list_native_targets()}
        self.assertEqual(set(matrix["routes"]), targets)
        for profile_id, routes in matrix["routes"].items():
            with self.subTest(profile=profile_id):
                self.assertEqual(set(routes), set(INTENT_METHODS))

    def test_known_profile_lookup(self):
        self.assertEqual(get_native_target("windows-11-uia").family, "windows")


if __name__ == "__main__":
    unittest.main()
