"""Kompilasi LaTeX dengan angka coverage aktual dan tolak bukti yang kedaluwarsa."""

import argparse
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def tex_escape(value):
    return str(value).replace("\\", "/").replace("_", r"\_").replace("%", r"\%")


def excerpt(path, names):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    return "\n\n".join(
        ast.get_source_segment(source, node)
        for node in tree.body if getattr(node, "name", None) in names
    ) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tectonic", default=shutil.which("tectonic"))
    args = parser.parse_args()
    if not args.tectonic:
        parser.error("Tectonic belum tersedia. Pasang Tectonic atau gunakan --tectonic PATH.")
    metadata = json.loads((ROOT / "reports/run-metadata.json").read_text(encoding="utf-8"))
    actual = {
        path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for folder in (ROOT / "src", ROOT / "tests") for path in sorted(folder.rglob("*.py"))
    }
    if actual != metadata["sha256"]:
        raise SystemExit("Source/test berubah. Jalankan python scripts/run_tests.py sebelum membangun laporan.")
    counts = metadata["result"]
    if counts["failures"] + counts["errors"] + counts["skipped"]:
        raise SystemExit("Laporan ini mensyaratkan test lulus tanpa error/skip. Periksa reports/pytest.txt.")
    cov = json.loads((ROOT / "reports/coverage.json").read_text(encoding="utf-8"))
    if cov["totals"] != metadata["coverage"]:
        raise SystemExit("Coverage JSON berbeda dengan metadata. Jalankan ulang pengujian.")
    generated = ROOT / "laporan/generated"
    generated.mkdir(parents=True, exist_ok=True)
    totals = cov["totals"]
    values = {
        "TestTotal": counts["tests"], "TestFailures": counts["failures"],
        "StatementTotal": totals["num_statements"], "StatementCovered": totals["covered_lines"],
        "BranchTotal": totals["num_branches"], "BranchCovered": totals["covered_branches"],
        "MissingLines": totals["missing_lines"], "MissingBranches": totals["missing_branches"],
        "RunAt": metadata["checked_at"], "PythonVersion": metadata["python"],
        "PytestVersion": metadata["tools"]["pytest"], "CovVersion": metadata["tools"]["coverage"],
        "PytestCovVersion": metadata["tools"]["pytest-cov"], "RunPlatform": metadata["platform"],
    }
    (generated / "results.tex").write_text("\n".join(
        chr(92) + "newcommand{" + chr(92) + key + "}{" + tex_escape(value) + "}"
        for key, value in values.items()
    ) + "\n", encoding="utf-8")
    rows = []
    for path, entry in sorted(cov["files"].items()):
        summary = entry["summary"]
        name = path.replace("\\", "/").rsplit("/", 1)[-1]
        branch_rate = (f'{100 * summary["covered_branches"] / summary["num_branches"]:.0f}' + r"\%"
                       if summary["num_branches"] else "--")
        rows.append(r"\texttt{" + tex_escape(name) + "} & " + " & ".join(map(str, [
            summary["num_statements"], summary["missing_lines"], summary["num_branches"],
            summary["missing_branches"], branch_rate,
        ])) + r" \\")
    table = (
        r"\begin{tabularx}{\linewidth}{@{}Yrrrrr@{}}" + "\n"
        + r"\toprule Modul & Stmt & Miss & Branch & MissBr & Branch \%\\\midrule" + "\n"
        + "\n".join(rows) + "\n"
        + r"\midrule Total & \StatementTotal & \MissingLines & \BranchTotal & \MissingBranches & 100\%\\\bottomrule" + "\n"
        + r"\end{tabularx}" + "\n"
    )
    (generated / "coverage-table.tex").write_text(table, encoding="utf-8")
    (generated / "scope-function.py").write_text(
        excerpt(ROOT / "src/zenta_auth/scopes.py", {"validate_scopes"}), encoding="utf-8")
    (generated / "basis-tests.py").write_text(
        excerpt(ROOT / "tests/test_scopes.py", {
            "test_p1_inactive_client_is_rejected", "test_p2_empty_scope_is_rejected",
            "test_p3_disallowed_scope_is_rejected", "test_p4_allowed_scopes_are_returned",
        }), encoding="utf-8")
    (generated / "subclasses.py").write_text(
        excerpt(ROOT / "src/zenta_auth/seller.py", {"FoodSellerApplication", "ClothingSellerApplication"}),
        encoding="utf-8")
    (generated / "state-test.py").write_text(
        excerpt(ROOT / "tests/test_seller.py", {"test_entire_transition_contract"}), encoding="utf-8")
    output = ROOT / "output/pdf"
    output.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        args.tectonic, "--keep-logs", "--outdir", str(output),
        str(ROOT / "laporan/laporan-sesi10-bambang.tex"),
    ], cwd=ROOT, check=True)
    print("PDF: " + str(output / "laporan-sesi10-bambang.pdf"))


if __name__ == "__main__":
    main()
