from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "lint_tikz_connectors.py"
FIXTURES = ROOT / "tests" / "fixtures"

spec = importlib.util.spec_from_file_location("lint_tikz_connectors", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ConnectorLintRegressionTest(unittest.TestCase):
    def test_named_connector_endpoints_pass(self) -> None:
        self.assertEqual(module.lint(FIXTURES / "good-named-connectors.tex"), [])

    def test_bad_case_rejects_magic_endpoints_and_excessive_arity(self) -> None:
        errors = module.lint(FIXTURES / "bad-hardcoded-connectors.tex")
        joined = "\n".join(errors)
        self.assertIn("maximum is 9", joined)
        self.assertIn("source must be a named node anchor", joined)
        self.assertIn("target must be a named node anchor", joined)


if __name__ == "__main__":
    unittest.main()
