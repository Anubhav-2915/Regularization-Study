"""experiment_log.py

Save a complete, reproducible record of every experiment, audit the results
folder, and pull numbers for the report straight from saved tables so that
no experimental number is ever typed by hand.

Put this file in  <project>/src/  and import it from a notebook with:

    import sys; sys.path.append("../src")
    from experiment_log import save_experiment_record, audit, lookup
"""
import json
import platform
import re
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

# ---- change this if your project lives somewhere else -----------------------
RESULTS_DIR = Path("D:/Research Project/results")
# -----------------------------------------------------------------------------

NA = "not applicable"
BAD_FIGURE_NAME = re.compile(r"^(image|figure|fig|plot|untitled|download|screenshot)[\s_\-]*\d*\.", re.I)

# Every record must state each of these (use a short "not applicable: reason" string if one truly does not apply).
REQUIRED = [
    "dataset", "preprocessing", "seeds", "models", "train_test_protocol",
    "cv_protocol", "metrics", "tables", "figures", "observation",
]


def set_results_dir(path):
    """Override the results folder for this session."""
    global RESULTS_DIR
    RESULTS_DIR = Path(path)


def _jsonable(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return None if np.isnan(o) else float(o)
    if isinstance(o, float):
        return None if np.isnan(o) else o
    if isinstance(o, np.ndarray):
        return [_jsonable(x) for x in o.tolist()]
    if isinstance(o, pd.DataFrame):
        return [_jsonable(r) for r in o.to_dict("records")]
    if isinstance(o, pd.Series):
        return _jsonable(o.to_dict())
    if isinstance(o, Path):
        return str(o)
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set, range)):
        return [_jsonable(x) for x in o]
    return o


def _environment():
    env = {"python": sys.version.split()[0], "platform": platform.platform()}
    for mod in ("numpy", "pandas", "sklearn", "scipy", "matplotlib"):
        try:
            env[mod] = __import__(mod).__version__
        except Exception:
            pass
    return env


def _fmt(v):
    if isinstance(v, dict):
        return "; ".join(f"{k}={_fmt(x)}" for k, x in v.items())
    if isinstance(v, list):
        return ", ".join(_fmt(x) for x in v)
    return str(v)


def _md_table(rows):
    cols = list(rows[0].keys())
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        cells = []
        for c in cols:
            v = r.get(c)
            cells.append(f"{v:.4f}" if isinstance(v, float) else str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def _to_markdown(rec):
    L = [f"# {rec['exp_id']}: {rec['title']}", f"_Saved: {rec['created']}_", ""]
    for key, head in [
        ("dataset", "Dataset"), ("preprocessing", "Preprocessing"),
        ("seeds", "Random seed(s)"), ("models", "Models and hyperparameters"),
        ("train_test_protocol", "Train/test protocol"), ("cv_protocol", "Cross-validation protocol"),
    ]:
        L += [f"## {head}", _fmt(rec[key]) if not isinstance(rec[key], dict) else
              "\n".join(f"- **{k}:** {_fmt(v)}" for k, v in rec[key].items()), ""]
    L += ["## Metrics"]
    m = rec["metrics"]
    if isinstance(m, list) and m and isinstance(m[0], dict):
        L.append(_md_table(m))
    else:
        L.append(_fmt(m))
    L += ["", "## Saved tables"] + [f"- results/tables/{t}" for t in rec["tables"]]
    L += ["", "## Saved figures"] + [f"- results/figures/{f}" for f in rec["figures"]]
    if rec["missing_files"]:
        L += ["", "## WARNING: files listed but not found", *[f"- {x}" for x in rec["missing_files"]]]
    L += ["", "## Observation", rec["observation"], ""]
    L += ["## Environment", _fmt(rec["environment"]), ""]
    return "\n".join(L)


def save_experiment_record(exp_id, title, *, dataset, preprocessing, seeds, models,
                           train_test_protocol, cv_protocol, metrics, tables, figures,
                           observation, notes=""):
    """Write results/experiments/<exp_id>.json and .md.

    Every field must be given. If something does not apply (e.g. CV in the
    gradient-descent experiment) pass a string such as
    "not applicable: no hyperparameter selection". `tables` and `figures` are
    lists of file names already saved in results/tables and results/figures.
    `metrics` can be a DataFrame, dict, or string pointing to the saved table.
    """
    supplied = dict(dataset=dataset, preprocessing=preprocessing, seeds=seeds, models=models,
                    train_test_protocol=train_test_protocol, cv_protocol=cv_protocol,
                    metrics=metrics, tables=tables, figures=figures, observation=observation)
    empty = [k for k in REQUIRED
             if supplied[k] is None
             or (isinstance(supplied[k], str) and not supplied[k].strip())
             or (isinstance(supplied[k], (list, dict)) and len(supplied[k]) == 0
                 and k not in ("figures", "tables"))]
    if empty:
        raise ValueError(f"Missing required fields: {empty}. Fill them in, or write "
                         f"'{NA}: <reason>' if a field truly does not apply.")

    missing = [f"tables/{t}" for t in tables if not (RESULTS_DIR / "tables" / t).exists()]
    missing += [f"figures/{f}" for f in figures if not (RESULTS_DIR / "figures" / f).exists()]
    bad_names = [f for f in figures if BAD_FIGURE_NAME.match(f)]

    rec = {
        "exp_id": exp_id, "title": title,
        "created": datetime.now().isoformat(timespec="seconds"),
        **supplied, "notes": notes, "missing_files": missing,
        "non_descriptive_figure_names": bad_names,
        "environment": _environment(),
    }
    rec = _jsonable(rec)

    out = RESULTS_DIR / "experiments"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{exp_id}.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
    (out / f"{exp_id}.md").write_text(_to_markdown(rec), encoding="utf-8")

    print(f"Saved results/experiments/{exp_id}.json and .md")
    if missing:
        print("WARNING - listed but not found:", missing)
    if bad_names:
        print("WARNING - rename these figures descriptively:", bad_names)
    return rec


def audit(expected_ids=None):
    """Check every saved record: files exist, observation written, figure names descriptive.
    Also lists files in results/ that no record mentions."""
    exp_dir = RESULTS_DIR / "experiments"
    rows, logged_t, logged_f, found = [], set(), set(), set()
    for p in sorted(exp_dir.glob("*.json")) if exp_dir.exists() else []:
        r = json.loads(p.read_text(encoding="utf-8"))
        found.add(r["exp_id"])
        logged_t.update(r["tables"])
        logged_f.update(r["figures"])
        miss = [f"tables/{t}" for t in r["tables"] if not (RESULTS_DIR / "tables" / t).exists()]
        miss += [f"figures/{f}" for f in r["figures"] if not (RESULTS_DIR / "figures" / f).exists()]
        rows.append({
            "experiment": r["exp_id"],
            "n_tables": len(r["tables"]), "n_figures": len(r["figures"]),
            "observation_written": bool(r["observation"].strip()),
            "missing_files": miss,
            "bad_figure_names": [f for f in r["figures"] if BAD_FIGURE_NAME.match(f)],
        })
    for e in (expected_ids or []):
        if e not in found:
            rows.append({"experiment": e, "n_tables": 0, "n_figures": 0,
                         "observation_written": False, "missing_files": ["NO RECORD SAVED"],
                         "bad_figure_names": []})
    on_disk_t = {p.name for p in (RESULTS_DIR / "tables").glob("*")} if (RESULTS_DIR / "tables").exists() else set()
    on_disk_f = {p.name for p in (RESULTS_DIR / "figures").glob("*")} if (RESULTS_DIR / "figures").exists() else set()
    unlogged = sorted([f"tables/{x}" for x in on_disk_t - logged_t] +
                      [f"figures/{x}" for x in on_disk_f - logged_f])
    if unlogged:
        print("Files on disk not listed in any experiment record:\n  " + "\n  ".join(unlogged))
    return pd.DataFrame(rows)


def lookup(csv_name, column, **where):
    """Read one value from a saved results table, e.g.
    lookup("feature_corr_summary.csv", "coef_error_mean", model="Ridge", rho=0.9)
    Use this (or the saved CSVs directly) for every number that goes in the report."""
    df = pd.read_csv(RESULTS_DIR / "tables" / csv_name)
    for k, v in where.items():
        if isinstance(v, (int, float, np.number)) and pd.api.types.is_numeric_dtype(df[k]):
            df = df[np.isclose(df[k].astype(float), float(v))]
        else:
            df = df[df[k] == v]
    if len(df) != 1:
        raise ValueError(f"Expected exactly 1 matching row in {csv_name}, found {len(df)}.")
    return df.iloc[0][column]