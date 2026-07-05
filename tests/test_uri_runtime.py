import json
import unittest

from urivision import CapabilityRegistry, default_runtime, register_uri_function, run_plan, uri_function
from urivision.uri import match_uri, parse_uri


class UriRuntimeTests(unittest.TestCase):
    def test_parse_and_match_uri(self):
        p = parse_uri("input://local/keyboard/command/type")
        self.assertEqual(p.scheme, "input")
        self.assertEqual(p.authority, "local")
        self.assertEqual(p.kind, "command")
        self.assertEqual(p.name, "type")
        self.assertEqual(match_uri("input://{target}/keyboard/command/type", p.raw), {"target": "local"})

    def test_catalog_has_runtime_capabilities(self):
        rt = default_runtime()
        catalog = rt.catalog("json")
        uris = [c["uri_pattern"] for c in catalog["capabilities"]]
        self.assertIn("runtime://{target}/capabilities/query/list", uris)
        self.assertIn("ui://{target}/element/query/find", uris)
        self.assertIn("guard://{target}/batch/command/run", uris)

    def test_call_find_and_type_and_verify(self):
        rt = default_runtime()
        found = rt.call("ui://local/element/query/find", {"role": "textbox", "name": "Search"})
        self.assertTrue(found["found"])
        rt.call("ui://local/element/command/focus", {"element_id": found["element"]["id"]})
        rt.call("input://local/keyboard/command/type", {"text": "hello"})
        verify = rt.call("view://local/screen/query/text", {"contains": "hello"})
        self.assertTrue(verify["found"])

    def test_plan_runner_template_reference(self):
        plan = {
            "steps": [
                {"id": "find", "call": "ui://local/element/query/find", "with": {"role": "button", "name": "Save"}, "expect_result": {"found": True}},
                {"id": "press", "call": "ui://local/element/command/press", "with": {"element_id": "${find.element.id}"}, "expect_result": {"ok": True}},
            ]
        }
        result = run_plan(plan, runtime=default_runtime())
        self.assertTrue(result["ok"])
        self.assertEqual(result["outputs"]["press"]["pressed"], "button:save")

    def test_function_binding(self):
        @uri_function("math://local/add/command/run", title="Add", description="Add two ints", kind="command")
        def add(a: int, b: int):
            return {"ok": True, "value": a + b}

        reg = CapabilityRegistry()
        register_uri_function(reg, add)
        result = reg.call("math://local/add/command/run", {"a": 2, "b": 4})
        self.assertEqual(result["value"], 6)


if __name__ == "__main__":
    unittest.main()
