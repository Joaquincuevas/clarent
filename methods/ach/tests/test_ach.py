"""ACH tests. Stdlib only: `python -m unittest discover -s methods/ach/tests` (from any directory)."""
import copy
import io
import json
import tempfile
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # run from any directory

from clarent_ach import ACHError, engine, i18n, main, parse
from clarent_ach.render import markdown

EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "flaky-test.json"
EXAMPLE_ES = EXAMPLE.with_name("flaky-test.es.json")


def setUpModule():
    i18n.set_lang("en")


def base():
    """Matriz mínima: A es contradicha, B no, 'O' es el comodín."""
    return {
        "hypotheses": [
            {"id": "A", "text": "a"},
            {"id": "B", "text": "b"},
            {"id": "O", "text": "otra", "catch_all": True},
        ],
        "evidence": [
            {"id": "E1", "text": "e1", "ref": "x", "credibility": "high", "relevance": "high",
             "ratings": {"A": "II", "B": "C", "O": "N"}},
        ],
    }


class ParseTests(unittest.TestCase):
    def test_requires_two_hypotheses(self):
        d = base(); d["hypotheses"] = d["hypotheses"][:1]
        with self.assertRaises(ACHError):
            parse(d)

    def test_duplicate_ids_rejected(self):
        d = base(); d["hypotheses"][1]["id"] = "A"
        with self.assertRaises(ACHError):
            parse(d)

    def test_unknown_hypothesis_in_ratings_rejected(self):
        d = base(); d["evidence"][0]["ratings"]["ZZ"] = "C"
        with self.assertRaises(ACHError):
            parse(d)

    def test_invalid_rating_rejected(self):
        d = base(); d["evidence"][0]["ratings"]["A"] = "MAYBE"
        with self.assertRaises(ACHError):
            parse(d)

    def test_all_catch_all_rejected(self):
        d = base()
        for h in d["hypotheses"]:
            h["catch_all"] = True
        with self.assertRaises(ACHError):
            parse(d)

    def test_uncited_observed_evidence_warns_and_strict_fails(self):
        d = base(); d["evidence"][0]["ref"] = ""
        self.assertTrue(any("without 'ref'" in w for w in parse(d).warnings))
        with self.assertRaises(ACHError):
            parse(d, strict=True)

    def test_missing_rating_assumed_neutral_with_warning(self):
        d = base(); del d["evidence"][0]["ratings"]["O"]
        an = parse(d)
        self.assertEqual(an.evidence[0].value("O"), 0)
        self.assertTrue(any("no rating" in w for w in an.warnings))


class ScoreTests(unittest.TestCase):
    def test_inconsistency_is_weighted_and_only_penalizes_inconsistent(self):
        res = engine.score(parse(base()))
        by = {s.id: s for s in res.scores}
        self.assertEqual(by["A"].inconsistency, 9 * 2)   # peso 3x3, II = 2
        self.assertEqual(by["B"].inconsistency, 0)
        self.assertEqual(res.leaders, ("B",))

    def test_consistent_evidence_never_changes_ranking(self):
        d = base()
        before = engine.score(parse(d))
        d["evidence"].append({"id": "E2", "text": "x", "ref": "r", "credibility": "high",
                              "relevance": "high", "ratings": {"A": "C", "B": "CC", "O": "C"}})
        after = engine.score(parse(d))
        self.assertEqual([(s.id, s.inconsistency) for s in before.scores],
                         [(s.id, s.inconsistency) for s in after.scores])

    def test_evidence_kinds(self):
        d = base()
        d["evidence"] += [
            {"id": "E2", "text": "igual", "ref": "r", "ratings": {"A": "C", "B": "C", "O": "C"}},
            {"id": "E3", "text": "solo apoya", "ref": "r", "ratings": {"A": "C", "B": "CC", "O": "N"}},
        ]
        kinds = {x.id: x.kind for x in engine.score(parse(d)).diagnostics}
        self.assertEqual(kinds, {"E1": "diagnostic", "E2": "non-diagnostic", "E3": "supports-only"})

    def test_catch_all_never_leads_but_warns(self):
        d = base()
        d["evidence"][0]["ratings"] = {"A": "II", "B": "II", "O": "N"}
        res = engine.score(parse(d))
        self.assertNotIn("O", res.leaders)
        self.assertTrue(any("catch-all" in w for w in res.warnings))

    def test_no_discrimination_when_all_equal(self):
        d = base(); d["evidence"][0]["ratings"] = {"A": "C", "B": "C", "O": "C"}
        res = engine.score(parse(d))
        self.assertEqual(res.verdict, "no-discrimination")

    def test_fragile_when_removing_one_evidence_flips_leader(self):
        d = base()
        d["evidence"] = [
            {"id": "E1", "text": "e1", "ref": "r", "credibility": "high", "relevance": "high",
             "ratings": {"A": "II", "B": "N", "O": "N"}},
            {"id": "E2", "text": "e2", "ref": "r", "credibility": "low", "relevance": "low",
             "ratings": {"A": "N", "B": "I", "O": "N"}},
            {"id": "E3", "text": "e3", "ref": "r", "credibility": "low", "relevance": "low",
             "ratings": {"A": "N", "B": "I", "O": "N"}},
            {"id": "E4", "text": "e4", "ref": "r", "credibility": "low", "relevance": "low",
             "ratings": {"A": "N", "B": "N", "O": "N"}},
        ]
        res = engine.score(parse(d))
        self.assertEqual(res.leaders, ("B",))
        self.assertTrue(res.fragile)   # sin E1, el líder pasa a ser A y B empata
        self.assertTrue(next(s for s in res.sensitivity if s.evidence_id == "E1").changes_leader)

    def test_deterministic(self):
        an = parse(json.loads(EXAMPLE.read_text(encoding="utf-8")))
        self.assertEqual(engine.score(an), engine.score(an))

    def test_proposed_evidence_does_not_affect_scores(self):
        d = base()
        d["evidence"].append({"id": "T1", "text": "t", "status": "proposed",
                              "ratings": {"A": "II", "B": "CC", "O": "N"}})
        with_t = engine.score(parse(d))
        without = engine.score(parse(base()))
        self.assertEqual([(s.id, s.inconsistency) for s in with_t.scores],
                         [(s.id, s.inconsistency) for s in without.scores])


class NextTestTests(unittest.TestCase):
    def test_example_golden(self):
        an = parse(json.loads(EXAMPLE.read_text(encoding="utf-8")))
        res = engine.score(an)
        self.assertEqual(res.leaders, ("H1", "H5"))
        self.assertEqual({s.id: s.inconsistency for s in res.scores},
                         {"H1": 0, "H5": 0, "H6": 0, "H2": 21, "H3": 27, "H4": 33})
        self.assertEqual({s.id for s in res.scores if s.refuted}, {"H2", "H3", "H4"})
        # T1 separa H1 de H5 -> primera. T3 trata igual a H1 y H5 -> descartada.
        self.assertEqual([t.id for t in res.next_tests], ["T1", "T2"])
        self.assertEqual(res.next_tests[0].priority, 36.0)

    def test_cost_lowers_priority(self):
        d = base()
        for cost, tid in (("low", "T1"), ("high", "T2")):
            d["evidence"].append({"id": tid, "text": tid, "status": "proposed", "cost": cost,
                                  "credibility": "high", "relevance": "high",
                                  "ratings": {"A": "CC", "B": "II", "O": "N"}})
        d["evidence"][0]["ratings"] = {"A": "N", "B": "N", "O": "N"}   # A y B siguen vivas
        res = engine.score(parse(d))
        self.assertEqual([t.id for t in res.next_tests], ["T1", "T2"])


class CliTests(unittest.TestCase):
    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            try:
                code = main(list(argv))
            except SystemExit as e:
                code = e.code
        return code, out.getvalue(), err.getvalue()

    def test_init_validate_score_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = str(Path(tmp) / "a.json")
            self.assertEqual(self.run_cli("init", p)[0], 0)
            self.assertEqual(self.run_cli("init", p)[0], 2)          # no sobrescribe
            self.assertEqual(self.run_cli("validate", p)[0], 0)
            code, out, _ = self.run_cli("score", p, "--format", "json")
            self.assertEqual(code, 0)
            self.assertIn("scores", json.loads(out))

    def test_bad_file_gives_clean_error_not_traceback(self):
        code, _, err = self.run_cli("score", "no-existe.json")
        self.assertEqual(code, 2)
        self.assertIn("error:", err)

    def test_markdown_report_has_key_sections(self):
        an = parse(json.loads(EXAMPLE.read_text(encoding="utf-8")))
        md = markdown(an, engine.score(an))
        for section in ("## Hypothesis ranking", "## Matrix", "## Sensitivity", "## Recommended next test", "not a probability"):
            self.assertIn(section, md)

    def test_example_is_valid_in_strict_mode(self):
        self.assertEqual(self.run_cli("validate", str(EXAMPLE), "--strict")[0], 0)

    def test_spanish_output_and_same_numbers(self):
        try:
            code_es, out_es, _ = self.run_cli("--lang", "es", "score", str(EXAMPLE_ES), "--format", "json")
            code_en, out_en, _ = self.run_cli("--lang", "en", "score", str(EXAMPLE), "--format", "json")
            self.assertEqual((code_es, code_en), (0, 0))
            strip = lambda o: [(s["id"], s["inconsistency"]) for s in json.loads(o)["scores"]]
            self.assertEqual(strip(out_es), strip(out_en))     # el idioma no cambia el cálculo
            _, md_es, _ = self.run_cli("--lang", "es", "score", str(EXAMPLE_ES))
            self.assertIn("## Ranking de hipótesis", md_es)
            self.assertIn("no una probabilidad", md_es)
        finally:
            i18n.set_lang("en")

    def test_unsupported_language_rejected(self):
        self.assertEqual(self.run_cli("--lang", "xx", "validate", str(EXAMPLE))[0], 2)   # argparse exit


if __name__ == "__main__":
    unittest.main()
