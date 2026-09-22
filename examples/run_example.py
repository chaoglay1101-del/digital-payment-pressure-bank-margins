"""Create and analyse a small synthetic bank panel for public demonstration."""

from pathlib import Path

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(__file__).resolve().parent / "example_panel.csv"


def build_example_panel() -> pd.DataFrame:
    """Return a deterministic, model-ready synthetic bank-year panel."""
    rng = np.random.default_rng(2026)
    banks = [f"BANK_{number:02d}" for number in range(1, 9)]
    years = range(2018, 2024)
    rows = []

    for bank_number, bank in enumerate(banks):
        bank_effect = rng.normal(0, 0.004)
        for year in years:
            digital_pressure = 20 + 1.8 * (year - 2018) + rng.normal(0, 1.2)
            capital = 0.08 + rng.normal(0, 0.01)
            size = 8.5 + bank_number * 0.18 + rng.normal(0, 0.04)
            credit_risk = 0.012 + rng.normal(0, 0.003)
            interest_expense = 0.025 + rng.normal(0, 0.004)
            deposit_ratio = 0.65 + rng.normal(0, 0.04)
            year_effect = (year - 2018) * 0.0005
            net_fee_margin = (
                0.018
                - 0.00015 * digital_pressure
                + 0.03 * capital
                - 0.01 * credit_risk
                + bank_effect
                + year_effect
                + rng.normal(0, 0.0015)
            )
            rows.append(
                {
                    "bank_id": bank,
                    "year": year,
                    "net_fee_margin": net_fee_margin,
                    "digital_payment_pressure": digital_pressure,
                    "capital_adequacy": capital,
                    "size": size,
                    "credit_risk": credit_risk,
                    "interest_expense_ratio": interest_expense,
                    "deposit_ratio": deposit_ratio,
                }
            )

    return pd.DataFrame(rows)


def estimate_example_model(panel: pd.DataFrame):
    """Estimate the fixed-effects model used in the public demonstration."""
    indexed_panel = panel.set_index(["bank_id", "year"])
    formula = (
        "net_fee_margin ~ 1 + digital_payment_pressure + capital_adequacy + "
        "size + credit_risk + interest_expense_ratio + deposit_ratio + "
        "EntityEffects + TimeEffects"
    )
    return PanelOLS.from_formula(formula=formula, data=indexed_panel).fit(
        cov_type="clustered",
        cluster_entity=True,
    )


def main() -> None:
    """Generate the public data file, fit the model, and report key diagnostics."""
    panel = build_example_panel()
    panel.to_csv(OUTPUT, index=False)
    result = estimate_example_model(panel)

    print(f"Wrote synthetic data to: {OUTPUT.relative_to(ROOT)}")
    print(f"Observations: {int(result.nobs)}")
    print(f"Banks: {panel['bank_id'].nunique()}")
    print("\nDigital payment pressure coefficient:")
    print(result.params["digital_payment_pressure"])
    print("\nThis is synthetic data for demonstrating the workflow, not thesis evidence.")


if __name__ == "__main__":
    main()
