"""TRIZ matrix tests. Stdlib only: `python -m unittest discover -s methods/triz-matrix/tests` (from any directory)."""
import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # run from any directory

from clarent_triz import TrizError, engine, i18n, load, main, resolve  # noqa: E402
from clarent_triz.model import DATA_DIR  # noqa: E402

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
M = load()


def setUpModule():
    i18n.set_lang("en")


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        try:
            code = main(list(argv))
        except SystemExit as e:
            code = e.code
    i18n.set_lang("en")
    return code, out.getvalue(), err.getvalue()


class DataIntegrity(unittest.TestCase):
    def test_catalog_is_complete_and_bilingual(self):
        self.assertEqual(sorted(M.params), list(range(1, 40)))
        self.assertEqual(sorted(M.principles), list(range(1, 41)))
        for p in M.params.values():
            for text in (p.en, p.es, p.sw_en, p.sw_es):
                self.assertTrue(text.strip(), f"parameter {p.id} has an empty field")
        for p in M.principles.values():
            for text in (p.en, p.es, p.desc_en, p.desc_es, p.sw_en, p.sw_es):
                self.assertTrue(text.strip(), f"principle {p.id} has an empty field")
        self.assertEqual(len({p.sw_en for p in M.principles.values()}), 40, "software examples must be distinct")

    def test_cells_are_classical_shape(self):
        for (i, j), c in M.cells.items():
            self.assertNotEqual(i, j)
            self.assertTrue(1 <= len(c.principles) <= 4, f"cell {i},{j} has {len(c.principles)} principles")
            self.assertEqual(len(set(c.principles)), len(c.principles))

    def test_documented_counts_match_the_data(self):
        counts = M.meta["counts"]
        self.assertEqual(counts["filled_cells"], len(M.cells))
        self.assertEqual(len(M.cells), 1248)       # matches the filled-cell count of 4 of the 5 independent sources
        for status in ("verified", "contested", "consensus"):
            self.assertEqual(counts[status], sum(1 for c in M.cells.values() if c.status == status))
        self.assertEqual(counts["contested"], 29)

    def test_contested_cells_carry_a_different_1973_reading(self):
        contested = [c for c in M.cells.values() if c.status == "contested"]
        self.assertTrue(contested)
        for c in contested:
            self.assertIsNotNone(c.alt)
            self.assertNotEqual(set(c.alt), set(c.principles))
        for c in M.cells.values():
            if c.status != "contested":
                self.assertIsNone(c.alt)

    def test_anchor_cells(self):
        """Cells present, unanimous and equal to the 1973 table in every source we cross-checked."""
        anchors = {(1, 3): (15, 8, 29, 34), (1, 5): (29, 17, 38, 34), (9, 36): (10, 28, 4, 34), (9, 27): (11, 35, 27, 28)}
        for cell, expected in anchors.items():
            self.assertEqual(M.cells[cell].principles, expected)
            self.assertEqual(M.cells[cell].status, "verified")
        self.assertNotIn((1, 2), M.cells)          # genuinely empty in the classical matrix

    def test_provenance_is_recorded(self):
        meta = M.meta
        self.assertEqual(len(meta["voting_sources"]), 5)
        for s in meta["voting_sources"]:
            self.assertRegex(s["commit"], r"^[0-9a-f]{40}$")
            self.assertRegex(s["sha256"], r"^[0-9a-f]{64}$")
            self.assertIn("MIT", s["license"])
            self.assertTrue(s["repo"].startswith("https://github.com/"))
        self.assertIn("altshuller.ru", meta["reference_source"]["url"])
        self.assertRegex(meta["reference_source"]["sha256"], r"^[0-9a-f]{64}$")

    def test_data_license_file_names_every_source_and_copyright_holder(self):
        text = (DATA_DIR / "DATA_LICENSE.md").read_text(encoding="utf-8")
        for s in M.meta["voting_sources"]:
            self.assertIn(s["repo"].replace("https://github.com/", ""), text)
        for holder in ("useful-skills contributors", "triz-engine contributors", "DoGyeong Seo", "magery.ai", "luchi2333"):
            self.assertIn(holder, text)
        self.assertIn("Permission is hereby granted", text)


class Resolve(unittest.TestCase):
    def test_by_number_name_and_language(self):
        self.assertEqual(resolve(M, "9")[0].id, 9)
        self.assertEqual(resolve(M, "Speed"), (M.params[9], "name"))
        self.assertEqual(resolve(M, "velocidad")[0].id, 9)
        self.assertEqual(resolve(M, "FIABILIDAD")[0].id, 27)
        self.assertEqual(resolve(M, "Complejidad del dispositivo")[0].id, 36)

    def test_accents_case_and_punctuation_are_ignored(self):
        self.assertEqual(resolve(M, "perdida de informacion")[0].id, 24)
        self.assertEqual(resolve(M, "  device   COMPLEXITY ")[0].id, 36)

    def test_aliases_and_unique_substrings(self):
        self.assertEqual(resolve(M, "Force")[0].id, 10)
        self.assertEqual(resolve(M, "composition")[0].id, 13)

    def test_software_words(self):
        p, how = resolve(M, "latency")
        self.assertEqual((p.id, how), (9, "software"))

    def test_ambiguous_is_an_error_that_lists_candidates(self):
        with self.assertRaises(TrizError) as cm:
            resolve(M, "weight")
        self.assertIn("1 Weight of moving object", str(cm.exception))
        self.assertIn("2 Weight of stationary object", str(cm.exception))
        with self.assertRaises(TrizError):
            resolve(M, "memory")                      # matches the software readings of 1 and 11

    def test_unknown_and_out_of_range(self):
        for bad in ("zzzz", "", "0", "40", "-1"):
            with self.assertRaises(TrizError, msg=bad):
                resolve(M, bad)
        with self.assertRaises(TrizError) as cm:
            resolve(M, "reliabilty")                  # typo -> suggestions
        self.assertIn("Reliability", str(cm.exception))


class Lookup(unittest.TestCase):
    def test_principles_keep_the_matrix_order(self):
        lk = engine.lookup(M, "Speed", "Device complexity")
        self.assertEqual(lk.kind, "principles")
        self.assertEqual([p.id for p in lk.principles], [10, 28, 4, 34])
        self.assertEqual(lk.status, "verified")

    def test_reverse_cell_is_reported(self):
        lk = engine.lookup(M, "Speed", "Device complexity")
        self.assertEqual([p.id for p in lk.reverse], [m for m in M.cells[(36, 9)].principles])

    def test_same_parameter_is_a_physical_contradiction(self):
        lk = engine.lookup(M, "Speed", "9")
        self.assertEqual(lk.kind, "same-parameter")
        self.assertEqual(lk.principles, ())

    def test_empty_cell(self):
        lk = engine.lookup(M, 1, 2)
        self.assertEqual((lk.kind, lk.principles), ("empty", ()))

    def test_contested_cell_exposes_both_readings(self):
        lk = engine.lookup(M, "Speed", "Weight of moving object")
        self.assertEqual(lk.status, "contested")
        self.assertEqual([p.id for p in lk.principles], [2, 28, 13, 38])
        self.assertEqual([p.id for p in lk.alt], [8, 28, 13, 38])

    def test_contested_cell_with_empty_1973_reading(self):
        lk = engine.lookup(M, "Adaptability or versatility", "Difficulty of detecting and measuring")
        self.assertEqual(lk.status, "contested")
        self.assertEqual(lk.alt, ())
        md = __import__("clarent_triz.render", fromlist=["x"]).lookup_markdown(lk)
        self.assertIn("no principles", md)

    def test_deterministic(self):
        self.assertEqual(engine.lookup(M, "Speed", "Reliability"), engine.lookup(M, "Speed", "Reliability"))


class Rank(unittest.TestCase):
    PAIRS = [("Speed", "Device complexity"), ("Speed", "Reliability"), ("Adaptability or versatility", "Device complexity")]

    def test_principle_in_every_contradiction_ranks_first(self):
        a = engine.rank(M, self.PAIRS)
        self.assertEqual((a.ranking[0].principle.id, a.ranking[0].count, a.ranking[0].pairs), (28, 3, (1, 2, 3)))

    def test_order_is_stable_and_counts_add_up(self):
        a = engine.rank(M, self.PAIRS)
        self.assertEqual(sum(r.count for r in a.ranking), sum(len(lk.principles) for lk in a.lookups))
        self.assertEqual(a.ranking, engine.rank(M, self.PAIRS).ranking)
        keys = [(-r.count, r.mean_position, r.principle.id) for r in a.ranking]
        self.assertEqual(keys, sorted(keys))

    def test_contested_flag_propagates(self):
        a = engine.rank(M, [("Speed", "Weight of moving object"), ("Speed", "Reliability")])
        flags = {r.principle.id: r.contested for r in a.ranking}
        self.assertTrue(flags[2])          # only in the contested cell
        self.assertFalse(flags[27])        # only in a verified cell

    def test_empty_and_same_pairs_contribute_nothing(self):
        a = engine.rank(M, [(1, 2), ("Speed", "Speed")])
        self.assertEqual(a.ranking, ())


class Cli(unittest.TestCase):
    def test_lookup_markdown(self):
        code, out, _ = run("lookup", "Speed", "Device complexity")
        self.assertEqual(code, 0)
        for s in ("## Principles", "Preliminary action", "Cell verified", "prompts for ideas", "Reverse cell"):
            self.assertIn(s, out)

    def test_lookup_json_is_stable(self):
        code, out, _ = run("lookup", "latency", "complexity", "--format", "json")
        self.assertEqual(code, 0)
        d = json.loads(out)
        self.assertEqual([p["id"] for p in d["principles"]], [10, 28, 4, 34])
        self.assertEqual((d["improving"]["resolved_by"], d["worsening"]["resolved_by"]), ("software", "name"))
        self.assertEqual(d["status"], "verified")
        self.assertIsNone(d["alternative_1973"])

    def test_spanish_changes_text_not_numbers(self):
        _, en, _ = run("--lang", "en", "lookup", "9", "36", "--format", "json")
        _, es, _ = run("--lang", "es", "lookup", "9", "36", "--format", "json")
        e, s = json.loads(en), json.loads(es)
        self.assertEqual([p["id"] for p in e["principles"]], [p["id"] for p in s["principles"]])
        self.assertNotEqual(e["principles"][0]["name"], s["principles"][0]["name"])
        self.assertEqual(s["principles"][0]["name"], "Acción previa")
        _, md, _ = run("--lang", "es", "lookup", "9", "36")
        self.assertIn("## Principios", md)

    def test_analyze_example_en_and_es_agree(self):
        c1, en, _ = run("analyze", str(EXAMPLES / "search-api.json"), "--format", "json")
        c2, es, _ = run("--lang", "es", "analyze", str(EXAMPLES / "search-api.es.json"), "--format", "json")
        self.assertEqual((c1, c2), (0, 0))
        ids = lambda o: [(r["principle"]["id"], r["count"]) for r in json.loads(o)["ranking"]]
        self.assertEqual(ids(en), ids(es))
        self.assertEqual(ids(en)[0], (28, 3))

    def test_analyze_markdown_has_one_section_per_contradiction(self):
        _, out, _ = run("analyze", str(EXAMPLES / "search-api.json"))
        self.assertEqual(len(re.findall(r"^## Contradiction \d", out, re.M)), 3)
        self.assertIn("SYNTHETIC EXAMPLE", out)

    def test_rank_with_pairs(self):
        code, out, _ = run("rank", "--pair", "Speed:Device complexity", "--pair", "Speed:Reliability", "--format", "json")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["ranking"][0]["principle"]["id"], 28)

    def test_errors_are_clean(self):
        for argv in (("lookup", "weight", "speed"), ("lookup", "nope", "speed"), ("analyze", "no-such.json"),
                     ("rank", "--pair", "SpeedReliability")):
            code, _, err = run(*argv)
            self.assertEqual(code, 2, argv)
            self.assertTrue(err.startswith("error:"), argv)

    def test_bad_analyze_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            for content in ("{not json", '{"pairs": []}', '{"pairs": [{"improving": "Speed"}]}', "[]"):
                bad.write_text(content, encoding="utf-8")
                self.assertEqual(run("analyze", str(bad))[0], 2, content)

    def test_params_and_principles_listings(self):
        _, out, _ = run("params", "--format", "json")
        self.assertEqual(len(json.loads(out)), 39)
        _, out, _ = run("principles", "--format", "json")
        self.assertEqual(len(json.loads(out)), 40)
        self.assertIn("39", run("params")[1])

    def test_init_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = str(Path(tmp) / "a" / "t.json")
            self.assertEqual(run("init", p)[0], 0)
            self.assertEqual(run("init", p)[0], 2)
            self.assertEqual(run("init", p, "--force")[0], 0)
            self.assertEqual(run("analyze", p)[0], 0)        # the template itself is analyzable

    def test_info_lists_sources(self):
        code, out, _ = run("info")
        self.assertEqual(code, 0)
        self.assertIn("1218 verified", out)
        self.assertIn("MIT", out)


class CustomData(unittest.TestCase):
    """Users who do not want to rely on the bundled matrix can supply their own."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_own_matrix_with_bundled_catalog(self):
        (self.tmp / "matrix.json").write_text(json.dumps({"cells": {"9,36": {"p": [1, 2], "n": 1, "s": "consensus"}}}), encoding="utf-8")
        code, out, _ = run("lookup", "Speed", "Device complexity", "--format", "json", "--data", str(self.tmp))
        self.assertEqual(code, 0)
        self.assertEqual([p["id"] for p in json.loads(out)["principles"]], [1, 2])

    def test_invalid_custom_data_is_rejected(self):
        for cells in ({"9,36": {"p": [99]}}, {"9,9": {"p": [1]}}, {"40,1": {"p": [1]}}, {"9,36": {"p": [1, 1]}},
                      {"9,36": {"p": [1], "s": "made-up"}}, {"x": {"p": [1]}}):
            (self.tmp / "matrix.json").write_text(json.dumps({"cells": cells}), encoding="utf-8")
            self.assertEqual(run("lookup", "9", "36", "--data", str(self.tmp))[0], 2, cells)

    def test_bundled_data_is_untouched_by_custom_runs(self):
        before = (DATA_DIR / "matrix.json").read_bytes()
        (self.tmp / "matrix.json").write_text(json.dumps({"cells": {}}), encoding="utf-8")
        run("lookup", "9", "36", "--data", str(self.tmp))
        self.assertEqual((DATA_DIR / "matrix.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
