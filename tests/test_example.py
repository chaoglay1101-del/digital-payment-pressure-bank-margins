"""Tests for the public synthetic research demonstration."""

import importlib.util
from pathlib import Path

import numpy as np

EXAMPLE_PATH = Path(__file__).resolve().parents[1] / "examples" / "run_example.py"
SPEC = importlib.util.spec_from_file_location("run_example", EXAMPLE_PATH)
assert SPEC is not None and SPEC.loader is not None
example = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(example)
build_example_panel = example.build_example_panel


def test_example_panel_has_expected_panel_structure() -> None:
    panel = build_example_panel()

    assert panel.shape == (48, 9)
    assert panel["bank_id"].nunique() == 8
    assert panel["year"].nunique() == 6
    assert not panel.duplicated(["bank_id", "year"]).any()


def test_example_panel_is_model_ready() -> None:
    panel = build_example_panel()
    expected_columns = {
        "bank_id",
        "year",
        "net_fee_margin",
        "digital_payment_pressure",
        "capital_adequacy",
        "size",
        "credit_risk",
        "interest_expense_ratio",
        "deposit_ratio",
    }

    assert set(panel.columns) == expected_columns
    numeric_columns = sorted(expected_columns - {"bank_id"})
    assert np.isfinite(panel[numeric_columns].to_numpy()).all()
    assert (panel["digital_payment_pressure"] > 0).all()
