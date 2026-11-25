"""Red team tests. Stdlib only: `python -m unittest discover -s methods/redteam/tests` (from any directory)."""
import copy
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # run from any directory

from clarent_redteam import RedTeamError, analyze, i18n, main, parse
from clarent_redteam import catalog, engine, model
from clarent_redteam.render import markdown

EX = Path(__file__).resolve().parent.parent / "examples"
DESIGN = EX / "design-doc" / "findings.json"
DESIGN_ES = EX / "design-doc" / "findings.es.json"
REJECTED = EX / "design-doc" / "findings.rejected.json"
PR = EX / "pr" / "findings.json"

TARGET = (
    "The worker retries failed jobs until they succeed.\n"
    "Jobs are processed in the order they were queued.\n"
    "Operators can roll back by switching the flag off.\n"
    "Peak load is under 100 jobs per minute.\n"
)


def setUpModule():
    i18n.set_lang("en")


class Workdir(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        (self.tmp / "t.md").write_text(TARGET, encoding="utf-8")

    def data(self):
        """Smallest valid file: two assumptions, one attack on each."""
        return {
            "target": {"files": ["t.md"]},
            "assumptions": [
                {"id": "A1", "text": "retries end", "quote": "retries failed jobs until they succeed", "status": "unverified",
                 "check": "send a job that always fails"},
                {"id": "A2", "text": "order holds", "quote": "processed in the order they were queued", "status": "unverified"},
            ],
            "attacks": [
                {"id": "X1", "class": "failure-modes", "assumption": "A1", "quote": "retries failed jobs until they succeed",
                 "attack": "a job that always fails is retried for ever and pins a worker", "impact": 3, "plausibility": 3,
                 "check": "enqueue a poison job and watch the worker"},
                {"id": "X2", "class": "scale", "assumption": "A2", "quote": "processed in the order they were queued",
                 "attack": "ordering forces a single consumer, so throughput cannot scale out", "impact": 2, "plausibility": 2,
                 "check": "run two consumers and compare the order"},
            ],
        }

    def run_engine(self, d):
        return analyze(parse(d, self.tmp))

    def codes(self, res):
        return {r.id: r.code for r in res.rejections}


# --------------------------------------------------------------------------- catalog
class CatalogTests(unittest.TestCase):
    def test_six_fixed_classes_in_order(self):
        self.assertEqual(catalog.CLASSES, ("key-assumptions", "failure-modes", "abuse", "scale", "dependency", "reversibility"))
        self.assertEqual(set(catalog.CATALOG), set(catalog.CLASSES))

    def test_every_class_is_bilingual_and_states_its_origin(self):
        for c, e in catalog.CATALOG.items():
            self.assertIn(e["origin"], ("handbook", "clarent"), c)
            self.assertTrue(e["pages"], c)
            for lang in ("en", "es"):
                self.assertTrue(e[lang]["name"] and e[lang]["question"], (c, lang))
                self.assertGreaterEqual(len(e[lang]["prompts"]), 3, (c, lang))

    def test_origin_is_honest_about_what_the_handbook_has(self):
        self.assertEqual({c for c, e in catalog.CATALOG.items() if e["origin"] == "clarent"},
                         {"scale", "dependency", "reversibility"})

    def test_rubrics_cover_1_to_5_in_both_languages(self):
        for key in ("impact", "plausibility"):
            for lang in ("en", "es"):
                self.assertEqual(sorted(catalog.RUBRIC[key][lang]), [1, 2, 3, 4, 5])

    def test_severity_bands(self):
        got = {r: catalog.severity(r) for r in (1, 5, 6, 11, 12, 19, 20, 25)}
        self.assertEqual(got, {1: "S4", 5: "S4", 6: "S3", 11: "S3", 12: "S2", 19: "S2", 20: "S1", 25: "S1"})
        self.assertTrue(catalog.at_least("S1", "S2"))
        self.assertFalse(catalog.at_least("S3", "S2"))

    def test_every_catalog_message_key_exists_in_both_languages(self):
        self.assertEqual(set(i18n.M["en"]), set(i18n.M["es"]))


# --------------------------------------------------------------------------- anchoring
class QuoteTests(unittest.TestCase):
    def files(self, text, name="t.md"):
        return (model.TargetFile(name, text, model._looks_like_diff(name, text)),)

    def test_whitespace_is_the_only_normalization(self):
        f = self.files("alpha beta\n   gamma\tdelta\nepsilon")
        self.assertEqual(model.find_quote(f, "beta gamma delta epsilon"), ("t.md", 1))
        self.assertIsNone(model.find_quote(f, "Beta gamma"))            # case matters
        self.assertIsNone(model.find_quote(f, "alpha gamma"))           # words must be adjacent

    def test_returns_the_line_where_the_quote_starts(self):
        f = self.files("one\ntwo three\nfour five six\n")
        self.assertEqual(model.find_quote(f, "five six")[1], 3)
        self.assertEqual(model.find_quote(f, "three four")[1], 2)

    def test_punctuation_counts(self):
        f = self.files("it is fine.\n")
        self.assertIsNotNone(model.find_quote(f, "it is fine."))
        self.assertIsNone(model.find_quote(f, "it is fine!"))

    def test_empty_quote_never_anchors(self):
        self.assertIsNone(model.find_quote(self.files("abc"), "   "))

    def test_diff_quote_without_markers_anchors_to_the_changed_line(self):
        diff = "diff --git a/x.py b/x.py\n--- a/x.py\n+++ b/x.py\n@@ -1,2 +1,3 @@\n context\n-old_call(a)\n+new_call(a)\n+other(b)\n"
        f = self.files(diff, "x.diff")
        self.assertEqual(model.find_quote(f, "new_call(a) other(b)"), ("x.diff", 7))
        self.assertEqual(model.find_quote(f, "+new_call(a)")[1], 7)      # with the marker also works (raw view)

    def test_diff_headers_are_not_code(self):
        diff = "diff --git a/x.py b/x.py\n--- a/x.py\n+++ b/x.py\n@@ -1 +1 @@\n+real_line_here\n"
        f = self.files(diff, "x.diff")
        self.assertIsNone(model.find_quote(f, "b/x.py @@ -1 +1 @@ real_line_here"))   # headers are not stripped into code

    def test_first_file_with_a_match_wins(self):
        f = (model.TargetFile("a.md", "nothing here", False), model.TargetFile("b.md", "x\nthe needle is here\n", False))
        self.assertEqual(model.find_quote(f, "the needle is here"), ("b.md", 2))


class RefTests(Workdir):
    def test_file_line_must_exist(self):
        self.assertEqual(model.check_ref("t.md:2", self.tmp), (True, ""))
        self.assertEqual(model.check_ref("t.md:1-4", self.tmp), (True, ""))
        self.assertEqual(model.check_ref("t.md:5", self.tmp), (False, "why_line:4"))
        self.assertEqual(model.check_ref("t.md:3-2", self.tmp)[0], False)
        self.assertEqual(model.check_ref("t.md:0", self.tmp)[0], False)
        self.assertEqual(model.check_ref("nope.md:1", self.tmp), (False, "why_not_found"))

    def test_refs_cannot_leave_the_root(self):
        self.assertEqual(model.check_ref("../t.md:1", self.tmp), (False, "why_outside"))

    def test_free_text_refs_are_accepted_but_empty_is_not(self):
        self.assertEqual(model.check_ref("pytest -n 4 tests/test_a.py", self.tmp), (True, ""))
        self.assertEqual(model.check_ref("kubectl logs web-1 | grep ERROR", self.tmp), (True, ""))
        self.assertEqual(model.check_ref("   ", self.tmp), (False, "why_empty"))


# --------------------------------------------------------------------------- parse
class ParseTests(Workdir):
    def assertRejectsInput(self, mutate):
        d = self.data()
        mutate(d)
        with self.assertRaises(RedTeamError):
            parse(d, self.tmp)

    def test_valid_minimum(self):
        f = parse(self.data(), self.tmp)
        self.assertEqual((len(f.assumptions), len(f.attacks), f.kind), (2, 2, "design"))

    def test_root_must_be_an_object(self):
        with self.assertRaises(RedTeamError):
            parse([], self.tmp)

    def test_unknown_schema_rejected(self):
        self.assertRejectsInput(lambda d: d.update(schema="clarent.redteam/9"))

    def test_target_problems(self):
        self.assertRejectsInput(lambda d: d.pop("target"))
        self.assertRejectsInput(lambda d: d["target"].update(files=[]))
        self.assertRejectsInput(lambda d: d["target"].update(files=["missing.md"]))
        self.assertRejectsInput(lambda d: d["target"].update(kind="blog"))

    def test_target_inside_the_file_cannot_leave_the_root(self):
        (self.tmp.parent / "secret.txt").write_text("secret", encoding="utf-8")
        self.addCleanup((self.tmp.parent / "secret.txt").unlink)
        self.assertRejectsInput(lambda d: d["target"].update(files=["../secret.txt"]))
        self.assertRejectsInput(lambda d: d["target"].update(files=[str(self.tmp.parent / "secret.txt")]))

    def test_target_option_overrides_the_file(self):
        d = self.data()
        d["target"] = {"files": ["missing.md"]}
        f = parse(d, self.tmp, targets=[str(self.tmp / "t.md")])
        self.assertEqual(len(f.files), 1)

    def test_structure_errors(self):
        self.assertRejectsInput(lambda d: d.update(assumptions=[]))
        self.assertRejectsInput(lambda d: d.update(attacks=[]))
        self.assertRejectsInput(lambda d: d["assumptions"][1].update(id="A1"))
        self.assertRejectsInput(lambda d: d["attacks"][1].update(id="X1"))
        self.assertRejectsInput(lambda d: d["attacks"][0].update(**{"class": "sql-injection"}))
        self.assertRejectsInput(lambda d: d["assumptions"][0].update(status="maybe"))
        self.assertRejectsInput(lambda d: d["attacks"][0].update(assumption="A9"))
        self.assertRejectsInput(lambda d: d["attacks"][0].pop("attack"))
        self.assertRejectsInput(lambda d: d["assumptions"][0].update(evidence="x"))
        self.assertRejectsInput(lambda d: d.update(skipped_classes=[{"class": "nope", "reason": "x"}]))

    def test_ratings_must_be_integers_from_1_to_5(self):
        for bad in (0, 6, -1, 2.5, "3", True, None):
            with self.subTest(bad=bad):
                self.assertRejectsInput(lambda d, bad=bad: d["attacks"][0].update(impact=bad))
                self.assertRejectsInput(lambda d, bad=bad: d["attacks"][0].update(plausibility=bad))

    def test_skipped_class_without_reason_warns_and_does_not_count(self):
        d = self.data()
        d["skipped_classes"] = [{"class": "abuse", "reason": ""}]
        f = parse(d, self.tmp)
        self.assertEqual(f.skipped, ())
        self.assertTrue(any("abuse" in w for w in f.warnings))

    def test_status_defaults_to_unverified(self):
        d = self.data()
        d["assumptions"][0].pop("status")
        self.assertEqual(parse(d, self.tmp).assumptions[0].status, "unverified")

    def test_diff_files_are_detected(self):
        (self.tmp / "c.diff").write_text("diff --git a/x b/x\n@@ -1 +1 @@\n+hello world again\n", encoding="utf-8")
        d = self.data()
        d["target"] = {"kind": "pr", "files": ["t.md", "c.diff"]}
        f = parse(d, self.tmp)
        self.assertEqual([x.is_diff for x in f.files], [False, True])


# --------------------------------------------------------------------------- engine
class RejectionTests(Workdir):
    def test_clean_input_has_no_rejections(self):
        res = self.run_engine(self.data())
        self.assertEqual(res.rejections, [])
        self.assertEqual(len(res.attacks), 2)

    def test_attack_without_quote_is_rejected(self):
        d = self.data(); d["attacks"][0]["quote"] = ""
        self.assertEqual(self.codes(self.run_engine(d)), {"X1": "quote_missing"})

    def test_attack_with_invented_quote_is_rejected(self):
        d = self.data(); d["attacks"][0]["quote"] = "the worker retries failed jobs ten times and then stops"
        self.assertEqual(self.codes(self.run_engine(d)), {"X1": "quote_not_found"})

    def test_short_quote_is_rejected(self):
        d = self.data(); d["attacks"][0]["quote"] = "retries"
        self.assertEqual(self.codes(self.run_engine(d)), {"X1": "quote_short"})

    def test_quote_of_exactly_the_minimum_length_is_accepted(self):
        (self.tmp / "t.md").write_text("abcdefghijkl and more text here\n", encoding="utf-8")
        d = self.data()
        d["assumptions"] = [d["assumptions"][0] | {"quote": "abcdefghijkl"}]
        d["attacks"] = [d["attacks"][0] | {"quote": "abcdefghijkl"}]
        self.assertEqual(self.run_engine(d).rejections, [])
        d["attacks"][0]["quote"] = "abcdefghijk"
        self.assertEqual(self.codes(self.run_engine(d)), {"X1": "quote_short"})

    def test_assumption_with_invented_quote_is_rejected_and_its_attacks_cascade(self):
        d = self.data(); d["assumptions"][0]["quote"] = "the worker never retries anything at all"
        self.assertEqual(self.codes(self.run_engine(d)), {"A1": "quote_not_found", "X1": "assumption_rejected"})

    def test_verified_and_contradicted_need_evidence(self):
        for status in ("verified", "contradicted"):
            with self.subTest(status=status):
                d = self.data(); d["assumptions"][0]["status"] = status
                self.assertEqual(self.codes(self.run_engine(d))["A1"], "no_evidence")

    def test_unverified_needs_no_evidence(self):
        self.assertNotIn("A2", self.codes(self.run_engine(self.data())))

    def test_evidence_with_a_ref_to_a_missing_line_rejects_the_assumption(self):
        d = self.data()
        d["assumptions"][0].update(status="contradicted", evidence=[{"ref": "t.md:40", "observation": "x"}])
        res = self.run_engine(d)
        self.assertEqual(self.codes(res)["A1"], "ref_invalid")
        self.assertIn("4 lines", next(r.detail for r in res.rejections if r.id == "A1"))

    def test_evidence_with_a_ref_to_a_missing_file_is_rejected(self):
        d = self.data()
        d["assumptions"][0].update(status="verified", evidence=[{"ref": "gone.py:3", "observation": "x"}])
        self.assertEqual(self.codes(self.run_engine(d))["A1"], "ref_invalid")

    def test_evidence_without_observation_or_ref_is_rejected(self):
        for ev in ({"ref": "t.md:1", "observation": ""}, {"ref": "", "observation": "saw it"}, {}):
            with self.subTest(ev=ev):
                d = self.data(); d["assumptions"][0].update(status="verified", evidence=[ev])
                self.assertEqual(self.codes(self.run_engine(d))["A1"], "ref_invalid")

    def test_free_text_evidence_is_accepted(self):
        d = self.data()
        d["assumptions"][0].update(status="verified", evidence=[{"ref": "pytest -k retry -x", "observation": "3 passed"}])
        self.assertEqual(self.run_engine(d).rejections, [])

    def test_attack_evidence_refs_are_checked_too(self):
        d = self.data(); d["attacks"][0]["evidence"] = [{"ref": "t.md:99", "observation": "x"}]
        self.assertEqual(self.codes(self.run_engine(d)), {"X1": "ref_invalid"})

    def test_attack_without_check_is_rejected(self):
        d = self.data(); d["attacks"][0]["check"] = ""
        self.assertEqual(self.codes(self.run_engine(d)), {"X1": "check_missing"})

    def test_near_duplicate_attacks_count_once(self):
        d = self.data()
        twin = copy.deepcopy(d["attacks"][0]); twin["id"] = "X3"
        twin["attack"] = "A job that always fails is retried for ever and pins a worker!"
        d["attacks"].append(twin)
        res = self.run_engine(d)
        self.assertEqual(self.codes(res), {"X3": "duplicate"})
        self.assertIn("X1", res.rejections[0].detail)

    def test_same_text_on_another_class_or_assumption_is_not_a_duplicate(self):
        d = self.data()
        twin = copy.deepcopy(d["attacks"][0]); twin["id"] = "X3"; twin["class"] = "scale"
        other = copy.deepcopy(d["attacks"][0]); other["id"] = "X4"; other["assumption"] = "A2"
        d["attacks"] += [twin, other]
        self.assertEqual(self.run_engine(d).rejections, [])

    def test_rejections_do_not_enter_scores_or_matrix(self):
        d = self.data(); d["attacks"][0]["quote"] = "this sentence is not in the target at all"
        res = self.run_engine(d)
        self.assertEqual([a.id for a in res.attacks], ["X2"])
        row = next(r for r in res.assumptions if r.id == "A1")
        self.assertTrue(all(not ids for ids in row.attacks_by_class.values()))


class ScoringTests(Workdir):
    def test_effective_plausibility_follows_the_assumption_status(self):
        self.assertEqual(engine.effective_plausibility(1, "contradicted"), 5)
        self.assertEqual(engine.effective_plausibility(5, "contradicted"), 5)
        self.assertEqual(engine.effective_plausibility(5, "verified"), 2)
        self.assertEqual(engine.effective_plausibility(1, "verified"), 1)       # never raised
        self.assertEqual(engine.effective_plausibility(4, "unverified"), 4)

    def test_risk_is_impact_times_effective_plausibility(self):
        d = self.data()
        d["assumptions"][0].update(status="contradicted", evidence=[{"ref": "t.md:1", "observation": "x"}])
        d["assumptions"][1].update(status="verified", evidence=[{"ref": "t.md:2", "observation": "x"}])
        d["attacks"][1].update(impact=4, plausibility=5)
        res = self.run_engine(d)
        by = {a.id: a for a in res.attacks}
        self.assertEqual((by["X1"].risk, by["X1"].effective_plausibility), (15, 5))
        self.assertEqual((by["X2"].risk, by["X2"].effective_plausibility), (8, 2))

    def test_ranking_breaks_ties_by_impact_then_evidence_then_id(self):
        d = self.data()
        d["attacks"][0].update(impact=3, plausibility=4)                   # 12
        d["attacks"][1].update(impact=4, plausibility=3)                   # 12, higher impact
        self.assertEqual([a.id for a in self.run_engine(d).attacks], ["X2", "X1"])
        d["attacks"][1].update(impact=3, plausibility=4)                   # 12 and 12, same impact
        d["attacks"][1]["evidence"] = [{"ref": "t.md:1", "observation": "x"}]
        self.assertEqual([a.id for a in self.run_engine(d).attacks], ["X2", "X1"])   # more evidence first
        d["attacks"][1]["evidence"] = []
        self.assertEqual([a.id for a in self.run_engine(d).attacks], ["X1", "X2"])   # then id

    def test_top_has_at_most_three_and_follows_the_ranking(self):
        d = self.data()
        for i in range(3, 7):
            x = copy.deepcopy(d["attacks"][0]); x["id"] = f"X{i}"; x["class"] = catalog.CLASSES[i % 6]
            x["attack"] = f"distinct failure number {i} with its own wording and details {i * 7}"
            x["impact"] = i - 1
            d["attacks"].append(x)
        res = self.run_engine(d)
        self.assertEqual(len(res.top), 3)
        self.assertEqual([a.id for a in res.top], [a.id for a in res.attacks[:3]])
        self.assertEqual([a.rank for a in res.attacks], list(range(1, len(res.attacks) + 1)))

    def test_worst_severity(self):
        res = self.run_engine(self.data())
        self.assertEqual(res.worst_severity, "S3")           # 3x3 = 9
        d = self.data(); d["attacks"][0].update(impact=5, plausibility=4)
        self.assertEqual(self.run_engine(d).worst_severity, "S1")

    def test_deterministic(self):
        a = engine.to_dict(self.run_engine(self.data()))
        b = engine.to_dict(self.run_engine(self.data()))
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))


class MatrixAndWarningTests(Workdir):
    def test_matrix_places_attacks_by_assumption_and_class(self):
        res = self.run_engine(self.data())
        row = {r.id: r for r in res.assumptions}
        self.assertEqual(row["A1"].attacks_by_class["failure-modes"], ("X1",))
        self.assertEqual(row["A2"].attacks_by_class["scale"], ("X2",))
        self.assertEqual(row["A1"].attacks_by_class["abuse"], ())
        self.assertEqual(row["A1"].where, "t.md:1")

    def test_uncovered_classes_warn_unless_skipped_with_a_reason(self):
        res = self.run_engine(self.data())
        self.assertEqual(sum("has no accepted attack" in w for w in res.warnings), 4)     # 6 classes - 2 covered
        d = self.data()
        d["skipped_classes"] = [{"class": c, "reason": "not applicable here"} for c in ("key-assumptions", "abuse", "dependency", "reversibility")]
        res = self.run_engine(d)
        self.assertEqual(sum("has no accepted attack" in w for w in res.warnings), 0)
        cov = {c.class_id: c for c in res.coverage}
        self.assertEqual(cov["abuse"].skipped_reason, "not applicable here")

    def test_skipping_a_class_that_has_attacks_warns(self):
        d = self.data(); d["skipped_classes"] = [{"class": "scale", "reason": "x"}]
        self.assertTrue(any("skipped and also has attacks" in w for w in self.run_engine(d).warnings))

    def test_assumption_without_attacks_warns(self):
        d = self.data(); d["attacks"] = d["attacks"][:1]
        self.assertTrue(any("A2 has no accepted attack" in w for w in self.run_engine(d).warnings))

    def test_few_assumptions_and_few_attacks_warn(self):
        w = self.run_engine(self.data()).warnings
        self.assertTrue(any("accepted assumptions" in x for x in w))
        self.assertTrue(any("top list has fewer than 3" in x for x in w))

    def test_unverified_assumption_without_check_warns(self):
        w = self.run_engine(self.data()).warnings
        self.assertTrue(any("A2 is unverified and has no 'check'" in x for x in w))
        self.assertFalse(any("A1 is unverified and has no 'check'" in x for x in w))

    def test_top_attacks_on_unverified_assumptions_are_flagged(self):
        w = self.run_engine(self.data()).warnings
        self.assertTrue(any("Top attacks rest on unverified assumptions (A1, A2)" in x for x in w))

    def test_verify_next_lists_unverified_assumptions_by_linked_risk(self):
        d = self.data()
        d["attacks"][1].update(impact=5, plausibility=4)
        v = self.run_engine(d).verify_next
        self.assertEqual([x.assumption for x in v], ["A2", "A1"])
        self.assertEqual(v[0].max_risk, 20)

    def test_verified_and_contradicted_assumptions_are_not_verify_next(self):
        d = self.data()
        d["assumptions"][0].update(status="contradicted", evidence=[{"ref": "t.md:1", "observation": "x"}])
        self.assertEqual([x.assumption for x in self.run_engine(d).verify_next], ["A2"])


# --------------------------------------------------------------------------- the shipped examples
class ExampleTests(unittest.TestCase):
    def analyze_file(self, path):
        return analyze(parse(json.loads(path.read_text(encoding="utf-8")), path.parent))

    def test_design_example_golden(self):
        res = self.analyze_file(DESIGN)
        self.assertEqual(res.rejections, [])
        self.assertEqual(res.status_counts(), {"verified": 1, "unverified": 3, "contradicted": 2})
        self.assertEqual([a.id for a in res.top], ["X3", "X1", "X2"])
        self.assertEqual([(a.id, a.risk, a.severity) for a in res.attacks],
                         [("X3", 25, "S1"), ("X1", 20, "S1"), ("X2", 16, "S2"), ("X4", 9, "S3"),
                          ("X5", 9, "S3"), ("X6", 8, "S3"), ("X7", 8, "S3")])
        self.assertTrue(all(c.attack_ids for c in res.coverage))                      # all six classes applied
        self.assertEqual([v.assumption for v in res.verify_next], ["A6", "A2", "A3"])

    def test_design_example_anchors_point_at_real_lines(self):
        res = self.analyze_file(DESIGN)
        where = {a.id: a.where for a in res.attacks}
        self.assertEqual(where["X1"], "design.md:19")
        self.assertEqual(where["X3"], "design.md:26")                                # the quote spans a line break

    def test_spanish_example_gives_the_same_ranking(self):
        es = self.analyze_file(DESIGN_ES)
        self.assertEqual(es.rejections, [])
        self.assertEqual([(a.id, a.risk) for a in es.attacks], [(a.id, a.risk) for a in self.analyze_file(DESIGN).attacks])

    def test_pr_example_golden(self):
        res = self.analyze_file(PR)
        self.assertEqual(res.rejections, [])
        self.assertEqual([a.id for a in res.top], ["X1", "X2", "X3"])
        self.assertEqual(res.worst_severity, "S2")
        cov = {c.class_id: c for c in res.coverage}
        self.assertTrue(cov["reversibility"].skipped_reason)
        self.assertFalse(any("has no accepted attack" in w for w in res.warnings))
        self.assertEqual({a.id: a.where for a in res.attacks}["X1"], "change.diff:15")   # anchored on the added line

    def test_rejected_example_is_refused_for_the_documented_reasons(self):
        res = self.analyze_file(REJECTED)
        self.assertEqual({r.id: r.code for r in res.rejections}, {
            "A3": "quote_not_found", "A4": "no_evidence", "A5": "ref_invalid",
            "X3": "assumption_rejected", "X4": "quote_short", "X5": "duplicate", "X6": "check_missing",
            "X7": "assumption_rejected", "X8": "assumption_rejected"})
        self.assertEqual([a.id for a in res.attacks], ["X1", "X2"])


# --------------------------------------------------------------------------- CLI and report
def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class CliTests(Workdir):
    def setUp(self):
        super().setUp()
        i18n.set_lang("en")
        self.path = self.tmp / "f.json"
        self.path.write_text(json.dumps(self.data()), encoding="utf-8")

    def tearDown(self):
        i18n.set_lang("en")

    def test_check_markdown_has_the_key_sections(self):
        code, out, _ = run("check", str(DESIGN))
        self.assertEqual(code, 0)
        for h in ("## Summary", "## Top 3 attacks by impact", "## Assumption matrix", "## Verify next",
                  "## All accepted attacks", "## Class coverage", "not a probability"):
            self.assertIn(h, out)
        self.assertNotIn("## Rejected findings", out)

    def test_check_json_is_stable_and_complete(self):
        code, out, _ = run("check", str(DESIGN), "--format", "json")
        d = json.loads(out)
        self.assertEqual((code, d["schema"], d["top"], d["worst_severity"]), (0, "clarent.redteam.report/1", ["X3", "X1", "X2"], "S1"))
        self.assertEqual(d["counts"], {"verified": 1, "unverified": 3, "contradicted": 2, "attacks": 7, "rejected": 0})
        self.assertEqual(len(d["coverage"]), 6)

    def test_rejections_exit_1_and_are_listed(self):
        code, out, _ = run("check", str(REJECTED))
        self.assertEqual(code, 1)
        self.assertIn("## Rejected findings", out)
        self.assertIn("line out of range (the file has 27 lines)", out)

    def test_validate_exit_codes(self):
        self.assertEqual(run("validate", str(DESIGN))[0], 0)
        code, out, _ = run("validate", str(REJECTED))
        self.assertEqual(code, 1)
        self.assertIn("rejected assumption A3", out)

    def test_fail_on_severity(self):
        self.assertEqual(run("check", str(DESIGN), "--fail-on", "S1")[0], 1)
        self.assertEqual(run("check", str(PR), "--fail-on", "S1")[0], 0)        # worst is S2
        self.assertEqual(run("check", str(PR), "--fail-on", "S2")[0], 1)
        code, _, err = run("check", str(PR), "--fail-on", "S9")
        self.assertEqual(code, 2)
        self.assertIn("--fail-on", err)

    def test_strict_fails_on_warnings(self):
        self.assertEqual(run("check", str(self.path))[0], 0)
        self.assertEqual(run("check", str(self.path), "--strict")[0], 1)

    def test_out_writes_a_file(self):
        out = self.tmp / "report.md"
        code, stdout, _ = run("check", str(DESIGN), "--out", str(out))
        self.assertEqual(code, 0)
        self.assertIn("report written", stdout)
        self.assertIn("# Red team", out.read_text(encoding="utf-8"))

    def test_top_prints_one_line_per_attack(self):
        code, out, _ = run("top", str(DESIGN))
        self.assertEqual(code, 0)
        self.assertEqual(len(out.strip().splitlines()), 3)
        self.assertTrue(out.startswith("1. X3 [S1 risk=25] (reversibility)"))

    def test_target_option_replaces_the_files_in_the_findings(self):
        other = self.tmp / "other.md"
        other.write_text("nothing relevant is written in this file\n", encoding="utf-8")
        code, out, _ = run("check", str(self.path), "--target", str(other))
        self.assertEqual(code, 1)                              # every quote is now missing
        self.assertIn("does not appear in the target", out)

    def test_root_option_moves_ref_resolution(self):
        d = self.data()
        d["assumptions"][0].update(status="verified", evidence=[{"ref": "sub/t.md:1", "observation": "x"}])
        (self.tmp / "sub").mkdir()
        (self.tmp / "sub" / "t.md").write_text("line\n", encoding="utf-8")
        self.path.write_text(json.dumps(d), encoding="utf-8")
        self.assertEqual(run("validate", str(self.path))[0], 0)
        self.assertEqual(run("validate", str(self.path), "--root", str(self.tmp / "sub"))[0], 1)   # sub/sub/t.md does not exist

    def test_bad_input_gives_a_clean_error_not_a_traceback(self):
        bad = self.tmp / "bad.json"
        bad.write_text("{not json", encoding="utf-8")
        for argv in (("check", str(bad)), ("check", str(self.tmp / "nope.json")), ("validate", str(bad))):
            code, out, err = run(*argv)
            self.assertEqual(code, 2, argv)
            self.assertTrue(err.startswith("error:"), argv)
            self.assertNotIn("Traceback", err)

    def test_init_creates_a_file_that_runs(self):
        out = self.tmp / "new" / "rt.json"
        code, stdout, _ = run("init", str(out), "--target", str(self.tmp / "t.md"))
        self.assertEqual(code, 0)
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data["schema"], "clarent.redteam/1")
        self.assertEqual(data["target"]["files"], ["t.md"])
        self.assertEqual(data["root"], "..")                       # the target is outside cwd: its own folder is the root
        self.assertEqual(run("validate", str(out))[0], 0)
        self.assertEqual(run("init", str(out), "--target", str(self.tmp / "t.md"))[0], 2)          # refuses to overwrite
        self.assertEqual(run("init", str(out), "--target", str(self.tmp / "t.md"), "--force")[0], 0)

    def test_init_needs_a_readable_target_with_a_usable_line(self):
        self.assertEqual(run("init", str(self.tmp / "a.json"), "--target", str(self.tmp / "missing.md"))[0], 2)
        (self.tmp / "tiny.md").write_text("hi\n", encoding="utf-8")
        self.assertEqual(run("init", str(self.tmp / "b.json"), "--target", str(self.tmp / "tiny.md"))[0], 2)

    def test_catalog_lists_the_six_classes_and_the_scales(self):
        code, out, _ = run("catalog")
        self.assertEqual(code, 0)
        for c in catalog.CLASSES:
            self.assertIn(c, out)
        self.assertIn("impact (1-5):", out)
        self.assertIn("plausibility (1-5):", out)
        self.assertIn("p. 151", out)

    def test_spanish_output_and_same_numbers(self):
        code, es, _ = run("--lang", "es", "check", str(DESIGN_ES), "--format", "json")
        en = json.loads(run("--lang", "en", "check", str(DESIGN_ES), "--format", "json")[1])
        self.assertEqual(json.loads(es)["top"], en["top"])
        code, md, _ = run("--lang", "es", "check", str(DESIGN_ES))
        self.assertIn("## Matriz de supuestos", md)
        self.assertIn("contradicho", md)
        self.assertIn("Reversibilidad", md)

    def test_unsupported_language_rejected(self):
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            main(["--lang", "xx", "catalog"])

    def test_table_cells_escape_pipes_and_newlines(self):
        d = self.data()
        d["attacks"][0]["attack"] = "a | b\nbroken table risk"
        self.path.write_text(json.dumps(d), encoding="utf-8")
        _, out, _ = run("check", str(self.path))
        self.assertIn("a \\| b broken table risk", out)


class CoreIntegrationTests(unittest.TestCase):
    def test_redteam_is_discovered_and_runs_through_the_core(self):
        root = Path(__file__).resolve().parents[3]
        sys.path.insert(0, str(root / "src"))
        from clarent import cli, registry
        self.assertIn("redteam", [m.id for m in registry.discover(root / "methods")])
        m = next(m for m in registry.discover(root / "methods") if m.id == "redteam")
        self.assertEqual(registry.doctor(m), [])
        out = io.StringIO()
        with redirect_stdout(out):
            code = cli.main(["redteam", "check", str(DESIGN), "--format", "json"])
        self.assertEqual((code, json.loads(out.getvalue())["top"]), (0, ["X3", "X1", "X2"]))


if __name__ == "__main__":
    unittest.main()
