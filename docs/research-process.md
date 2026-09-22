# Research Process

This page maps the public repository to the research decisions behind the final undergraduate project.

## 1. Scope and design

The project examines the association between digital payment pressure and bank net fee margins. It was designed as an ASEAN-5 study, but the final panel covers **Indonesia, Malaysia, and Thailand (ASEAN-3)** because the selected IMF FAS measure was not consistently available for the Philippines and Singapore.

The public repository documents the workflow and provides a synthetic demonstration. Course submissions, drafts, restricted bank data, and derived thesis datasets remain outside the public code surface.

## 2. Bank-panel construction

[src/data/prepare_bank_panel.py](../src/data/prepare_bank_panel.py) reads a restricted WRDS-derived bank panel and a candidate bank list, filters the intended countries, normalises bank names, and calculates financial variables including:

- liquidity ratio;
- loan-to-deposit ratio;
- capital-adequacy proxy; and
- net fee margin.

It produces `Academic_Bank_Panel_Data_Cleaned.csv`. The required source files and output are excluded because they contain data that cannot be redistributed in this portfolio.

## 3. Digital-payment indicator

The indicator workflow separates discovery from the final measurement choice:

1. [src/data/download_imf_fas.py](../src/data/download_imf_fas.py) retrieves the public IMF FAS wide-format source file.
2. [src/data/discover_fas_indicator.py](../src/data/discover_fas_indicator.py) searches indicator labels by relevant keywords.
3. [src/data/extract_digital_payment_pressure.py](../src/data/extract_digital_payment_pressure.py) extracts `IMF_FAS_FCMIBT` with unit `PT_GDP` to form a country-year digital-payment-pressure measure.

This separation makes the measurement decision inspectable rather than treating the selected variable as a black box. IMF outputs are not committed to the repository; users should review the source's current access and redistribution terms.

## 4. Merge and validation

[src/data/merge_bank_panel.py](../src/data/merge_bank_panel.py) maps bank observations to countries and joins country-year payment pressure to the cleaned bank panel. The merge enforces a many-to-one country-year relationship to prevent duplicated indicator observations.

The merged panel is an intermediate research output and is excluded from public version control.

## 5. Main regression analysis

[src/analysis/run_main_regressions.py](../src/analysis/run_main_regressions.py) implements the final specifications. It:

- builds a common complete-case estimation sample;
- calculates credit risk, interest expense, deposit, scaled, and log measures;
- winsorises continuous variables at the 1st and 99th percentiles;
- estimates bank and year fixed-effects models with bank-clustered standard errors; and
- reports log, bank-size interaction, and mean-centred nonlinear specifications.

The exact input dataset is restricted, so this script is retained for transparency but cannot run from a public clone.

## 6. Country-subsample robustness

[src/analysis/run_country_subsamples.py](../src/analysis/run_country_subsamples.py) estimates the log specification separately for Indonesia, Malaysia, and Thailand. It retains bank fixed effects and excludes year effects because the country-year explanatory measure would otherwise be absorbed in a single-country model.

## 7. Public demonstration

[examples/run_example.py](../examples/run_example.py) creates a deterministic synthetic panel and estimates a simplified bank and year fixed-effects model with bank-clustered standard errors.

```powershell
uv sync --group dev
uv run python examples/run_example.py
uv run pytest
```

The generated coefficient and data are illustrative only; they are not thesis evidence.

## Public-release checklist

- [x] Exclude restricted bank data, derived datasets, course submissions, and local environments.
- [x] Provide a deterministic synthetic example and an automated test for the public workflow.
- [x] Clearly distinguish the public demonstration from the non-public thesis results.
- [ ] Confirm current WRDS, IMF, university, and any other relevant redistribution permissions before publishing additional data or artefacts.
- [ ] Check the final GitHub file list and rendered README before every public release.
- [ ] Replace the optional citation metadata in `CITATION.cff` with preferred author details if a formal citation is required.
