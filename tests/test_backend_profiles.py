import unittest

from urivision import DEFAULT_MATRIX, default_runtime, get_backend_profile, list_backend_profiles


class BackendProfileTests(unittest.TestCase):
    def test_default_matrix_has_four_profiles(self):
        self.assertEqual(len(DEFAULT_MATRIX), 4)
        self.assertIn("linux-x11-novnc", DEFAULT_MATRIX)
        self.assertIn("linux-wayland-headless", DEFAULT_MATRIX)
        self.assertIn("windows-uia-contract", DEFAULT_MATRIX)
        self.assertIn("macos-ax-contract", DEFAULT_MATRIX)

    def test_platform_profile_capability(self):
        rt = default_runtime(state={"backend_profile": "linux-x11-novnc"})
        result = rt.call("runtime://local/platform/query/profile", {})
        self.assertTrue(result["ok"])
        self.assertEqual(result["profile"]["name"], "linux-x11-novnc")
        self.assertEqual(result["profile"]["os_family"], "linux")

    def test_health_check_for_all_matrix_profiles(self):
        for profile in DEFAULT_MATRIX:
            with self.subTest(profile=profile):
                rt = default_runtime(state={"backend_profile": profile})
                result = rt.call("runtime://local/health/query/check", {"profile": profile})
                self.assertTrue(result["ok"])
                self.assertTrue(result["passed"])

    def test_list_backend_profiles(self):
        profiles = {p.name for p in list_backend_profiles()}
        for name in DEFAULT_MATRIX:
            self.assertIn(name, profiles)
            self.assertEqual(get_backend_profile(name).name, name)


if __name__ == "__main__":
    unittest.main()
