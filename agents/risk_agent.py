import pandas as pd

PARTICIPATION_MAP = {"Low": 0.2, "Medium": 0.55, "High": 0.9}


def compute_risk_score(row: pd.Series) -> float:
    """
    Compute 0–100 risk score from the real 36-column CSV.
    CSV already has risk_score pre-computed — this function lets you
    re-compute or verify it using raw columns.

    Weights:
      Attendance gap   : 30%
      Quiz performance : 25%
      Late submissions : 20%
      Participation    : 15%
      Days since login : 10%
    """
    attendance  = float(row.get("attendance_pct", 100))
    quiz_avg    = float(row.get("quiz_avg", 100))
    late_sub    = float(row.get("late_submissions", 0))
    total       = float(row.get("total_assignments", 1))
    days_login  = float(row.get("days_since_login", 0))

    part_raw = row.get("participation_level", row.get("participation", "Medium"))
    if isinstance(part_raw, str):
        participation = PARTICIPATION_MAP.get(part_raw, 0.55)
    else:
        participation = float(part_raw)

    # Normalise days_since_login: cap at 30 days
    login_norm = min(days_login / 30.0, 1.0)

    risk = (
        (1 - attendance / 100)      * 30 +
        (1 - quiz_avg / 100)        * 25 +
        (late_sub / max(total, 1))  * 20 +
        (1 - participation)         * 15 +
        login_norm                  * 10
    )
    return round(min(max(risk, 0), 100), 2)


def compute_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Re-compute risk scores from raw columns.
    Use this if you want to override the CSV's pre-computed risk_score.
    """
    df = df.copy()
    df["risk_score_computed"] = df.apply(compute_risk_score, axis=1)
    return df


def _risk_label(score: float) -> str:
    if score >= 65:
        return "High Risk"
    elif score >= 35:
        return "Medium Risk"
    else:
        return "Low Risk"
