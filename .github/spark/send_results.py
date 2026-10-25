"""Run check50 on every weekN/weekN_*.py file and send the results to the SPARK grading sheet."""
import glob
import json
import os
import subprocess
import sys
import urllib.request

CHECKS_REPO = os.environ.get("CHECKS_REPO", "camananyi/spark-checks/main")
SHEET_URL = os.environ.get("SHEET_URL", "")
SHEET_TOKEN = os.environ.get("SHEET_TOKEN", "")


def run_check50(path):
    """Return check50's results for one assignment file, or None if there are no checks for it."""
    folder, filename = os.path.split(path)
    slug = filename[:-3]
    try:
        proc = subprocess.run(
            ["check50", "--local", f"{CHECKS_REPO}/{slug}", "-o", "json"],
            cwd=folder or ".", capture_output=True, text=True, timeout=300,
        )
    except subprocess.TimeoutExpired:
        print(f"  {slug}: check50 took too long, skipped")
        return None
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(f"  {slug}: no checks found, skipped")
        return None
    if not data.get("results"):
        print(f"  {slug}: no checks found, skipped")
        return None

    checks = []
    for r in data["results"]:
        cause = r.get("cause") or {}
        if r["passed"] is None:
            # check50 skips a check when one it depends on failed
            note = "not checked yet, fix the earlier problems first"
        else:
            parts = [x.strip() for x in (cause.get("rationale"), cause.get("help")) if x]
            note = " ".join(p if p.endswith((".", "!", "?")) else p + "." for p in parts)
        checks.append({
            "name": r["name"],
            "description": r["description"],
            "passed": r["passed"] is True,
            "note": note,
        })
        print(f"  {':)' if r['passed'] else ':('} {r['description']}")
    return {"assignment": slug, "checks": checks}


def main():
    files = sorted(glob.glob("week*/week*.py"))
    if not files:
        print("No assignment files found (expected names like week1/week1_aboutme.py).")
        return

    submissions = []
    for path in files:
        print(f"Checking {path}")
        result = run_check50(path)
        if result:
            submissions.append(result)

    if not submissions:
        print("Nothing to send.")
        return
    if not SHEET_URL.startswith(("https://", "http://")):
        print("SHEET_URL is not set in the workflow file, so results were not sent.")
        sys.exit(1)

    payload = {
        "token": SHEET_TOKEN,
        "github_user": os.environ.get("GITHUB_REPOSITORY_OWNER", ""),
        "repo": os.environ.get("GITHUB_REPOSITORY", ""),
        "commit": os.environ.get("GITHUB_SHA", "")[:7],
        "submissions": submissions,
    }
    req = urllib.request.Request(
        SHEET_URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"},
    )
    # Apps Script answers with a redirect; urllib follows it and returns the script's reply
    with urllib.request.urlopen(req, timeout=60) as resp:
        reply = resp.read().decode()
    print("Grading sheet replied:", reply)
    if '"ok":true' not in reply.replace(" ", ""):
        sys.exit(1)


if __name__ == "__main__":
    main()
