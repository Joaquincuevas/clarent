"""Segunda pasada: consultas dirigidas a candidatos del top 10. Uso: python github_scan2.py out.json"""
import json, subprocess, sys, time, datetime
QS = [
 "analysis of competing hypotheses claude", "analysis of competing hypotheses debugging", "competing hypotheses root cause llm",
 "STPA software llm", "STPA unsafe control actions tool", "system-theoretic process analysis claude",
 "theory of constraints bottleneck ci pipeline", "theory of constraints software delivery tool", "drum buffer rope software",
 "FMEA claude skill", "FMEA source code analysis llm", "failure mode effects analysis software module",
 "fault tree analysis incident postmortem llm", "fault tree minimal cut sets python",
 "kepner tregoe problem analysis is is not", "is/is not problem specification debugging",
 "cynefin claude skill", "cynefin router agent",
 "commander's intent subagent prompt", "mission command agent orchestration delegation",
 "control chart ci build time western electric", "statistical process control ci flaky tests",
 "reference class forecasting git history estimate", "estimate cycle time from git history monte carlo",
 "red team design review claude skill", "devil's advocate agent claude code skill", "ufmcs red teaming",
 "ARIZ contradiction software architecture", "TRIZ software architecture contradiction llm",
 "after action review incident hook claude", "postmortem generator from git incident",
 "delphi method llm agents estimation", "design structure matrix python import graph",
 "wardley map generate from code", "heilmeier catechism proposal rfc",
 "hypothesis-driven debugging claude skill", "scientific method debugging skill claude",
]
def search(q):
    r = subprocess.run(["gh","api","-X","GET","search/repositories","-f",f"q={q}","-f","sort=stars","-f","per_page=5"],capture_output=True,text=True,encoding="utf-8")
    if r.returncode: return {"error": r.stderr[:200], "items": []}
    return {"items":[{"repo":i["full_name"],"stars":i["stargazers_count"],"pushed":i["pushed_at"][:10],"archived":i["archived"],"lang":i["language"],"desc":(i["description"] or "")[:150]} for i in json.loads(r.stdout)["items"]]}
out={"scanned_at":datetime.date.today().isoformat(),"results":{}}
for q in QS:
    res=search(q)
    if "error" in res and "rate" in res["error"].lower(): time.sleep(60); res=search(q)
    out["results"][q]=res; time.sleep(2.3)
json.dump(out,open(sys.argv[1],"w",encoding="utf-8"),indent=1,ensure_ascii=False)
print("DONE")
