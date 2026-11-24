"""Escanea GitHub por metodologia: top repos por estrellas (generico + enfoque agente/dev).
Uso: python github_scan.py out.json   (requiere gh autenticado). Rate limit search: 30/min."""
import json, subprocess, sys, time, datetime

Q = {
 "ooda": ['OODA loop', 'OODA loop claude agent'],
 "mission-command": ['"mission command" auftragstaktik', 'commander intent agent prompt'],
 "mdmp": ['"military decision making process"', 'MDMP planning llm'],
 "aar": ['"after action review"', 'after action review postmortem generator'],
 "red-team-ufmcs": ['"red teaming" design review llm agent', 'red team agent claude code'],
 "premortem": ['premortem', 'pre-mortem claude skill'],
 "carver": ['CARVER target analysis', 'CARVER threat prioritization'],
 "wargaming": ['wargame decision simulation llm', 'wargaming agents'],
 "center-of-gravity": ['"center of gravity" strategy analysis', 'critical vulnerabilities analysis'],
 "ipb": ['intelligence preparation battlefield', 'IPB threat modeling'],
 "jidoka-poka-yoke": ['poka-yoke software', 'jidoka andon software'],
 "andon": ['andon cord ci', 'andon board devops'],
 "kaizen": ['kaizen retrospective tool', 'kaizen engineering'],
 "five-whys": ['"5 whys" root cause', '5 whys llm agent'],
 "ishikawa": ['ishikawa fishbone diagram', 'fishbone root cause tool'],
 "a3": ['A3 problem solving toyota', 'A3 thinking template'],
 "hoshin-kanri": ['hoshin kanri', 'hoshin kanri okr'],
 "smed": ['SMED single minute exchange of die', 'SMED software deploy'],
 "pdca": ['PDCA plan do check act', 'PDCA claude'],
 "spc": ['statistical process control charts', 'SPC control chart ci metrics'],
 "triz": ['TRIZ', 'TRIZ llm', 'TRIZ claude skill'],
 "ariz": ['ARIZ altshuller', 'ARIZ-85 algorithm inventive problem solving'],
 "su-field": ['su-field analysis TRIZ', 'substance field TRIZ'],
 "evolution-laws": ['laws of technical systems evolution TRIZ', 'trends of engineering system evolution'],
 "otsm-triz": ['OTSM-TRIZ', 'OTSM TRIZ thinking'],
 "tectology": ['bogdanov tectology', 'tektology'],
 "fmea": ['FMEA failure mode effects analysis', 'FMEA software llm'],
 "fta": ['fault tree analysis', 'fault tree analysis llm'],
 "nasa-se": ['NASA systems engineering handbook', 'systems engineering requirements verification llm'],
 "stpa": ['STPA Leveson', 'STPA hazard analysis tool'],
 "toc": ['theory of constraints', 'drum buffer rope', 'theory of constraints ci bottleneck'],
 "kepner-tregoe": ['kepner tregoe', 'kepner-tregoe decision analysis'],
 "cynefin": ['cynefin framework', 'cynefin tool'],
 "wardley": ['wardley maps', 'wardley map llm'],
 "delphi": ['delphi method estimation', 'delphi method llm'],
 "fermi": ['fermi estimation', 'fermi estimation llm'],
 "superforecasting": ['superforecasting forecasting', 'forecasting llm calibration'],
 "ach": ['"analysis of competing hypotheses"', 'ACH competing hypotheses debugging'],
 "key-assumptions-check": ['"key assumptions check" structured analytic techniques', 'structured analytic techniques'],
 "six-hats": ['six thinking hats', 'six thinking hats llm'],
 "morphological": ['morphological analysis zwicky', 'morphological box design space'],
 "pugh-matrix": ['pugh matrix decision', 'pugh matrix tool'],
 "qfd": ['quality function deployment house of quality', 'QFD requirements'],
 "axiomatic-design": ['axiomatic design nam suh', 'axiomatic design software'],
 "reference-class": ['reference class forecasting', 'reference class forecasting estimation'],
 "hazop": ['HAZOP', 'hazop software'],
 "vsm-beer": ['viable system model stafford beer', 'viable system model'],
 "requisite-variety": ['ashby requisite variety', 'law of requisite variety'],
 "causal-loop": ['causal loop diagram system dynamics', 'system dynamics modeling tool'],
 "critical-chain": ['critical chain project management', 'critical chain buffer'],
 "heilmeier": ['heilmeier catechism', 'heilmeier catechism research'],
 "bowtie": ['bowtie risk analysis', 'bow-tie barrier analysis'],
 "apollo-rca": ['apollo root cause analysis', 'cause mapping root cause'],
 "scamper": ['SCAMPER creativity', 'scamper llm'],
 "kantorovich-lp": ['linear programming kantorovich', 'optimization planning llm'],
 "reflexive-control": ['reflexive control lefebvre', 'reflexive theory lefebvre'],
 "deep-battle-operational-art": ['soviet operational art deep battle', 'operational art planning'],
 "dsm": ['design structure matrix', 'design structure matrix dependency'],
 "taguchi": ['taguchi robust design', 'taguchi method'],
 "rdm-rand": ['robust decision making deep uncertainty', 'decision making under deep uncertainty'],
 "kill-chain-f3ead": ['F3EAD find fix finish', 'kill chain analysis'],
 "value-stream-mapping": ['value stream mapping', 'value stream mapping software delivery'],
 "gilb-evo": ['Tom Gilb Planguage', 'Evo evolutionary delivery gilb'],
}

def search(q):
    r = subprocess.run(["gh","api","-X","GET","search/repositories","-f",f"q={q}","-f","sort=stars","-f","per_page=5"],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        return {"error": r.stderr.strip()[:200], "items": []}
    items = json.loads(r.stdout).get("items", [])
    return {"items": [{"repo": i["full_name"], "stars": i["stargazers_count"], "pushed": i["pushed_at"][:10],
            "archived": i["archived"], "lang": i["language"], "desc": (i["description"] or "")[:140]} for i in items]}

out = {"scanned_at": datetime.date.today().isoformat(), "results": {}}
for mid, qs in Q.items():
    out["results"][mid] = {}
    for q in qs:
        res = search(q)
        if "error" in res and "rate limit" in res["error"].lower():
            time.sleep(60); res = search(q)
        out["results"][mid][q] = res
        time.sleep(2.3)
    print(mid, flush=True)
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("DONE")
