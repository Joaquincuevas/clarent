"""Core tests: discovery, doctor (positive and negative cases), and delegation to a method CLI.

Run from the repo root:  python -m unittest discover -s tests
"""
import datetime as dt
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from clarent import cli, registry  # noqa: E402

ACH_DIR = ROOT / "methods" / "ach"


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = cli.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class TempMethods(unittest.TestCase):
    """Each test gets a private copy of the ach method to break on purpose."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        shutil.copytree(ACH_DIR, self.tmp / "ach", ignore=shutil.ignore_patterns("__pycache__"))

    def method(self):
        return registry.discover(self.tmp)[0]

    def problems(self):
        return registry.doctor(self.method())


class DiscoveryTests(unittest.TestCase):
    def test_ach_is_discovered(self):
        ids = [m.id for m in registry.discover(ROOT / "methods")]
        self.assertIn("ach", ids)

    def test_list_command(self):
        code, out, _ = run("list")
        self.assertEqual(code, 0)
        self.assertIn("ach", out)

    def test_list_json(self):
        code, out, _ = run("list", "--format", "json")
        self.assertEqual(code, 0)
        self.assertTrue(any(m["id"] == "ach" for m in json.loads(out)))


class DoctorTests(TempMethods):
    def test_reference_method_is_healthy(self):
        self.assertEqual(self.problems(), [])

    def test_missing_card_section_is_reported(self):
        card = self.tmp / "ach" / "CARD.md"
        card.write_text(card.read_text(encoding="utf-8").replace("## Limitations", "## Notes"), encoding="utf-8")
        self.assertTrue(any("Limitations" in p for p in self.problems()))

    def test_missing_card_is_reported(self):
        (self.tmp / "ach" / "CARD.md").unlink()
        self.assertTrue(any("CARD.md is missing" in p for p in self.problems()))

    def test_blocked_or_read_source_without_url_is_reported(self):
        mf = self.tmp / "ach" / "method.toml"
        mf.write_text(mf.read_text(encoding="utf-8") + '\n[[sources]]\ntitle = "x"\nverification = "read"\n', encoding="utf-8")
        self.assertTrue(any("requires a url" in p for p in self.problems()))

    def test_invented_verification_level_is_rejected(self):
        mf = self.tmp / "ach" / "method.toml"
        text = mf.read_text(encoding="utf-8").replace('verification = "read"', 'verification = "trust-me"', 1)
        mf.write_text(text, encoding="utf-8")
        self.assertTrue(any("verification must be one of" in p for p in self.problems()))

    def test_stale_novelty_claim_is_a_warning_not_a_failure(self):
        late = dt.date(2027, 6, 1)   # > 90 days after the 2026-11-24 scan
        self.assertEqual(self.problems(), [])                                  # doctor stays green
        self.assertTrue(any("days old" in w for w in registry.stale_claims(self.method(), late)))
        self.assertEqual(registry.stale_claims(self.method(), dt.date(2026, 12, 1)), [])

    def test_long_skill_description_is_reported(self):
        sk = self.tmp / "ach" / "skill" / "SKILL.md"
        text = sk.read_text(encoding="utf-8").replace("description: ", "description: " + "x" * 400 + " ", 1)
        sk.write_text(text, encoding="utf-8")
        self.assertTrue(any("max 300" in p for p in self.problems()))

    def test_missing_tests_and_examples_are_reported(self):
        shutil.rmtree(self.tmp / "ach" / "tests")
        shutil.rmtree(self.tmp / "ach" / "examples")
        probs = self.problems()
        self.assertTrue(any("tests/" in p for p in probs))
        self.assertTrue(any("examples/" in p for p in probs))

    def test_id_must_match_folder(self):
        mf = self.tmp / "ach" / "method.toml"
        mf.write_text(mf.read_text(encoding="utf-8").replace('id = "ach"', 'id = "other"', 1), encoding="utf-8")
        self.assertTrue(any("must equal folder name" in p for p in self.problems()))

    def test_doctor_command_exit_codes(self):
        self.assertEqual(run("doctor", "ach")[0], 0)      # staleness never fails by default
        self.assertEqual(run("doctor", "nope")[0], 2)


class DelegationTests(unittest.TestCase):
    EXAMPLE = str(ACH_DIR / "examples" / "flaky-test.json")

    def test_ach_validate_through_core(self):
        code, out, _ = run("ach", "validate", self.EXAMPLE, "--strict")
        self.assertEqual(code, 0)
        self.assertIn("6 hypotheses", out)

    def test_ach_score_through_core_matches_expected_leaders(self):
        code, out, _ = run("ach", "score", self.EXAMPLE, "--format", "json")
        self.assertEqual(code, 0)
        self.assertEqual(tuple(json.loads(out)["leaders"]), ("H1", "H5"))

    def test_unknown_command(self):
        code, _, err = run("does-not-exist")
        self.assertEqual(code, 2)
        self.assertIn("unknown command", err)


if __name__ == "__main__":
    unittest.main()
