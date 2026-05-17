import pandas as pd
import numpy as np
import streamlit as st

# ── Required columns — app cannot work without these ─────────────────────────
REQUIRED_COLS = [
    "name", "grade", "subject",
    "attendance_pct", "quiz_avg", "overall_score"
]

# ── Optional columns — auto-computed if missing ───────────────────────────────
OPTIONAL_DEFAULTS = {
    "student_id":          lambda df: [f"STU{1001+i}" for i in range(len(df))],
    "section":             lambda df: ["A"] * len(df),
    "semester":            lambda df: ["Current"] * len(df),
    "participation_level": lambda df: ["Medium"] * len(df),
    "late_submissions":    lambda df: [0] * len(df),
    "missing_assignments": lambda df: [0] * len(df),
    "total_assignments":   lambda df: [8] * len(df),
    "midterm_score":       lambda df: df["overall_score"],
    "final_exam_score":    lambda df: df["overall_score"],
    "assignment_avg":      lambda df: df["overall_score"],
    "weak_topic":          lambda df: df["subject"],
    "second_weak_topic":   lambda df: df["subject"],
    "days_since_login":    lambda df: [0] * len(df),
    "parent_phone":        lambda df: ["N/A"] * len(df),
    "parent_email":        lambda df: ["N/A"] * len(df),
}

PARTICIPATION_MAP = {"Low": 0.2, "Medium": 0.55, "High": 0.9}


def _compute_risk_score(row) -> float:
    attendance    = float(row.get("attendance_pct", 100))
    quiz_avg      = float(row.get("quiz_avg", 100))
    late_sub      = float(row.get("late_submissions", 0))
    total         = float(row.get("total_assignments", 8))
    days_login    = float(row.get("days_since_login", 0))
    part_raw      = row.get("participation_level", "Medium")
    participation = PARTICIPATION_MAP.get(str(part_raw), 0.55)
    login_norm    = min(days_login / 30.0, 1.0)
    risk = (
        (1 - attendance / 100)     * 30 +
        (1 - quiz_avg / 100)       * 25 +
        (late_sub / max(total, 1)) * 20 +
        (1 - participation)        * 15 +
        login_norm                 * 10
    )
    return round(min(max(risk, 0), 100), 2)


def _risk_label(score: float) -> str:
    if score >= 65:   return "High Risk"
    elif score >= 35: return "Medium Risk"
    else:             return "Low Risk"


def validate_and_prepare(df: pd.DataFrame):
    """
    Validate uploaded CSV, fill missing optional columns, compute risk.
    Returns (prepared_df, warnings_list, missing_required_cols_list)
    """
    df = df.copy()
    warnings      = []
    missing_cols  = [c for c in REQUIRED_COLS if c not in df.columns]

    if missing_cols:
        return df, [], missing_cols

    # Fill optional columns that are absent
    for col, default_fn in OPTIONAL_DEFAULTS.items():
        if col not in df.columns:
            df[col] = default_fn(df)
            warnings.append(f"'{col}' not found — auto-filled with defaults")

    # Fill NaN assignment columns with 0
    assign_cols = [c for c in df.columns if c.startswith("assignment_") and c != "assignment_avg"]
    df[assign_cols] = df[assign_cols].fillna(0)

    # Ensure numeric participation column
    if "participation" not in df.columns:
        df["participation"] = df["participation_level"].map(PARTICIPATION_MAP).fillna(0.55)

    # Compute risk_score and risk_level if not present
    if "risk_score" not in df.columns:
        df["risk_score"] = df.apply(_compute_risk_score, axis=1)
        warnings.append("'risk_score' not found — computed from attendance, quiz, submissions, and participation")

    if "risk_level" not in df.columns:
        df["risk_level"] = df["risk_score"].apply(_risk_label)
        warnings.append("'risk_level' not found — computed from risk_score")

    return df, warnings, []


# ── Public API — all pages call these ─────────────────────────────────────────

def load_students() -> pd.DataFrame:
    """
    Return the DataFrame stored in session_state after upload.
    Raises a clear error if no data has been uploaded yet.
    """
    if "df" not in st.session_state or st.session_state["df"] is None:
        raise RuntimeError("NO_DATA")
    return st.session_state["df"]


def get_at_risk_students(threshold: float = 35.0) -> pd.DataFrame:
    df = load_students()
    return (
        df[df["risk_score"] >= threshold]
        .sort_values("risk_score", ascending=False)
        .reset_index(drop=True)
    )


def get_student_by_id(student_id: str) -> dict:
    df = load_students()
    row = df[df["student_id"] == student_id]
    return row.iloc[0].to_dict() if not row.empty else {}


def summary_stats() -> dict:
    df = load_students()
    total       = len(df)
    high_risk   = int((df["risk_level"] == "High Risk").sum())
    medium_risk = int((df["risk_level"] == "Medium Risk").sum())
    low_risk    = int((df["risk_level"] == "Low Risk").sum())
    avg_overall = round(df["overall_score"].mean(), 1)
    return {
        "total_students":    total,
        "high_risk":         high_risk,
        "medium_risk":       medium_risk,
        "low_risk":          low_risk,
        "avg_overall_score": avg_overall,
        "total":             total,       # legacy key
        "avg_overall":       avg_overall, # legacy key
    }
