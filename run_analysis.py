"""Run the selected thesis notebooks offline, each in an isolated Python process."""
from __future__ import annotations

import argparse
import base64
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parent


def run_worker(path: Path, quick: bool, update_notebooks: bool) -> int:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd

    notebook = json.loads(path.read_text(encoding="utf-8"))
    output_dir = ROOT / "results" / "rerun" / path.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    scope = {"__name__": "__main__", "__file__": str(path)}
    log_parts = []
    exports = {}
    failed = False
    current_outputs = []
    plot_counter = 0

    def capture_plots(*args, **kwargs):
        nonlocal plot_counter
        for figure_id in plt.get_fignums():
            figure = plt.figure(figure_id)
            image = io.BytesIO()
            figure.savefig(image, format="png", dpi=110, bbox_inches="tight")
            png = image.getvalue()
            plot_counter += 1
            (output_dir / f"display_{plot_counter:02d}.png").write_bytes(png)
            current_outputs.append({"output_type": "display_data", "metadata": {},
                                    "data": {"image/png": base64.b64encode(png).decode("ascii"),
                                             "text/plain": [f"<Figure {figure_id}>\n"]}})
        plt.close("all")

    plt.show = capture_plots
    os.chdir(ROOT)
    execution_count = 0
    table_names = {"df_comparison", "vif_data", "df_lp", "df_with_controls", "df_without_controls",
                   "df_surprises_results", "df_results", "results_df", "comparison_placebo", "table"}
    for index, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] != "code":
            continue
        if quick and "slow" in cell.get("metadata", {}).get("tags", []):
            cell["execution_count"] = None
            cell["outputs"] = []
            log_parts.append(f"Cell {index}: skipped Monte Carlo simulation (--quick).\n")
            continue
        current_outputs = []
        execution_count += 1
        buffer = io.StringIO()
        error = None
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            try:
                source = "".join(cell["source"])
                exec(compile(source, f"{path.name}:cell{index}", "exec"), scope)
            except BaseException as exc:
                if isinstance(exc, KeyboardInterrupt):
                    raise
                error = exc
                traceback.print_exc()
        text = buffer.getvalue()
        log_parts.append(f"\n=== Cell {index} ===\n{text}")
        cell["execution_count"] = execution_count
        cell["outputs"] = ([{"output_type": "stream", "name": "stdout", "text": text.splitlines(True)}]
                           if text else []) + current_outputs
        if error is not None or any(marker in text for marker in [
            "❌ Fatal error", "❌ Could not fit", "ERRORE durante", "ERROR loading data", "❌ Error:",
        ]):
            failed = True
            break

        for name in table_names:
            value = scope.get(name)
            if isinstance(value, pd.DataFrame):
                frame = value
            elif isinstance(value, list) and value and isinstance(value[0], (dict, list)):
                frame = pd.DataFrame(value)
            else:
                continue
            if len(frame) <= 100:
                frame.to_csv(output_dir / f"cell{index:02d}_{name}.csv", index=True)
        for name in ["result_break1", "result_break2", "r_nom", "r_adj"]:
            value = scope.get(name)
            if isinstance(value, dict):
                exports[f"cell{index:02d}_{name}"] = value
        for name in ["results_parsimonious", "results_full"]:
            value = scope.get(name)
            if hasattr(value, "params") and hasattr(value, "rsquared_adj"):
                exports[f"cell{index:02d}_{name}"] = {
                    "coefficients": value.params.to_dict(), "p_values": value.pvalues.to_dict(),
                    "z_statistics": value.tvalues.to_dict(), "adjusted_r_squared": value.rsquared_adj,
                    "observations": value.nobs,
                }

    (output_dir / "execution.log").write_text("".join(log_parts), encoding="utf-8")
    (output_dir / "numeric_results.json").write_text(
        json.dumps(exports, ensure_ascii=False, indent=2, default=float) + "\n", encoding="utf-8")
    executed_path = output_dir / "executed.ipynb"
    executed_path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if update_notebooks and not failed:
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{'FAILED' if failed else 'OK'}: {path.name} — {output_dir.relative_to(ROOT)}", flush=True)
    if failed:
        print("See execution.log for the error.", flush=True)
    return int(failed)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="Run one notebook, using its filename stem or numeric prefix, e.g. 03")
    parser.add_argument("--quick", action="store_true", help="Skip the 1,000-iteration TVL placebo simulation")
    parser.add_argument("--update-notebooks", action="store_true", help="Also refresh displayed outputs in notebooks/")
    parser.add_argument("--worker", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        return run_worker(Path(args.worker), args.quick, args.update_notebooks)

    paths = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if args.only:
        paths = [p for p in paths if p.stem == args.only or p.stem.startswith(args.only + "_")]
        if len(paths) != 1:
            parser.error("--only must identify exactly one notebook.")
    cache = ROOT / "results" / "rerun" / ".matplotlib"
    cache.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, MPLBACKEND="Agg", MPLCONFIGDIR=str(cache),
               OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
    failures = []
    for path in paths:
        print(f"Running {path.name}...", flush=True)
        command = [sys.executable, str(Path(__file__).resolve()), "--worker", str(path)]
        if args.quick:
            command.append("--quick")
        if args.update_notebooks:
            command.append("--update-notebooks")
        result = subprocess.run(command, cwd=ROOT, env=env, check=False)
        if result.returncode:
            failures.append(path.name)
    print(f"Completed {len(paths) - len(failures)}/{len(paths)} notebooks.", flush=True)
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
