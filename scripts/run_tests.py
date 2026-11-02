"""Jalankan PyTest satu kali dan simpan bukti coverage aktual, termasuk metadata."""

import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)
command = [
    sys.executable, "-m", "pytest", "-v", "--color=no", "--cov=zenta_auth", "--cov-branch",
    "--cov-report=term-missing", "--cov-report=html:htmlcov",
    "--cov-report=json:reports/coverage.json", "--cov-report=xml:reports/coverage.xml",
    "--junitxml=reports/junit.xml", "--cov-fail-under=100",
]
result = subprocess.run(
    command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    env={**os.environ, "PYTHONIOENCODING": "utf-8"},
)
output = result.stdout + result.stderr
(REPORTS / "pytest.txt").write_text(output, encoding="utf-8")
print(output, end="")
if result.returncode:
    raise SystemExit(result.returncode)

report = subprocess.run(
    [sys.executable, "-m", "coverage", "report"], cwd=ROOT,
    capture_output=True, text=True, encoding="utf-8", check=True,
)
(REPORTS / "coverage.txt").write_text(report.stdout, encoding="utf-8")
coverage = json.loads((REPORTS / "coverage.json").read_text(encoding="utf-8"))
suites = ET.parse(REPORTS / "junit.xml").getroot().findall("testsuite")
counts = {key: sum(int(suite.get(key, "0")) for suite in suites)
          for key in ("tests", "failures", "errors", "skipped")}
hashes = {
    path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
    for folder in (ROOT / "src", ROOT / "tests") for path in sorted(folder.rglob("*.py"))
}
metadata = {
    "checked_at": datetime.now(timezone(timedelta(hours=7))).isoformat(timespec="seconds"),
    "timezone": "Asia/Bangkok (UTC+07:00)",
    "python": platform.python_version(), "platform": platform.system(),
    "tools": {name: importlib.metadata.version(name) for name in ("pytest", "pytest-cov", "coverage")},
    "command": "python " + " ".join(command[1:]), "result": counts,
    "coverage": coverage["totals"], "sha256": hashes,
}
(REPORTS / "run-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
assert coverage["totals"]["missing_lines"] == 0
assert coverage["totals"]["missing_branches"] == 0
