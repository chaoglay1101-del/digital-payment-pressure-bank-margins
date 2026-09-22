# Digital Payment Pressure and Bank Net Fee Margins

**Research portfolio | Undergraduate accounting and finance project | ASEAN-3 bank panel**

[繁體中文版](README.zh-TW.md)

This project studies whether digital-payment activity is associated with banks' net fee margins in **Indonesia, Malaysia, and Thailand**. It combines bank-level financial data with an IMF Financial Access Survey (FAS) country-year measure, then estimates fixed-effects panel regressions to distinguish the relationship from persistent bank differences and common time trends.

> **Research question:** Is digital payment pressure associated with bank net fee margins in Indonesia, Malaysia, and Thailand?

## Why it matters

Digital payments can create transaction opportunities for banks while also increasing competition for traditional payment fees. Rather than assume one outcome, this project tests the association in an ASEAN-3 bank panel.

## Key findings

The final thesis sample contains **344 observations from 39 banks between 2014 and 2022**.

- Linear specifications provide limited evidence of a direct association.
- The log specification identifies a negative, statistically significant pooled association.
- Country subsamples are heterogeneous, and decomposition analysis suggests the pooled relationship may substantially reflect cross-country structural differences rather than a common within-country effect.

These are **conditional associations, not causal estimates**. The country-level explanatory measure, limited country coverage, omitted variables, and data constraints limit causal interpretation.

| Specification | Digital payment coefficient | Observations | Interpretation |
| --- | ---: | ---: | --- |
| Main model, scaled measure | -0.000292* | 344 | Negative association; marginal statistical evidence |
| Main model with controls | -0.000264 | 344 | Negative association; not statistically significant |
| Full controls model | -0.000208 | 344 | Negative association; not statistically significant |
| Log baseline model | -0.010171** | 344 | Negative and statistically significant pooled association |
| Nonlinear model | -0.010829** | 344 | Negative linear term; squared term not significant |

`* p < 0.10`, `** p < 0.05`.

## Research design

1. Construct bank-level net fee margins and financial controls from the restricted bank panel.
2. Identify IMF FAS indicator `IMF_FAS_FCMIBT`, measured as mobile and internet banking transactions as a percentage of GDP (`PT_GDP`).
3. Merge the country-year measure with bank-year observations.
4. Estimate bank and year fixed-effects models with bank-clustered standard errors and 1st/99th percentile winsorisation.
5. Assess log, interaction, nonlinear, and country-subsample specifications.

The detailed decision trail is in [docs/research-process.md](docs/research-process.md).

## Reproducibility and data access

| Component | Publicly reproducible? | Notes |
| --- | --- | --- |
| Synthetic fixed-effects demonstration | Yes | Fully self-contained in [examples/run_example.py](examples/run_example.py). |
| IMF FAS retrieval and indicator extraction | Partly | The source is public but availability and terms can change; outputs are intentionally not committed. |
| Bank-panel construction and thesis regressions | No | Required WRDS-derived data and intermediate files are restricted and excluded. |
| Reported thesis findings | Inspectable, not rerunnable | This README reports the final results, but public files cannot regenerate them without the restricted inputs. |

The study was originally designed for ASEAN-5. The final analysis is ASEAN-3 because the selected IMF measure was not consistently available for the Philippines and Singapore.

## Run the public example

The public example uses deterministic **synthetic** data. Its output demonstrates the Python and `linearmodels` workflow only; it is not evidence for the thesis.

### Requirements

- Python 3.14
- [uv](https://docs.astral.sh/uv/)

```powershell
uv sync --group dev
uv run python examples/run_example.py
uv run pytest
```

The example writes an ignored `examples/example_panel.csv` file and estimates a fixed-effects model with bank-clustered standard errors.

## Repository layout

```text
examples/                 Runnable synthetic-data demonstration
src/data/                 Restricted-panel preparation and IMF FAS workflow
src/analysis/             Final thesis regression and robustness specifications
tests/                    Checks for the public synthetic demonstration
docs/research-process.md  Research decisions, scope, and data-access notes
```

The intended restricted-data workflow is:

```text
prepare bank panel -> download/discover/extract IMF indicator -> merge panel
-> run main regressions -> run country robustness checks
```

## Methods and tools

Python 3.14+, pandas, NumPy, linearmodels, statsmodels, matplotlib, openpyxl, and python-docx. Dependency metadata and reproducible environment resolution are in [pyproject.toml](pyproject.toml) and [uv.lock](uv.lock).

## Academic and data note

This is an academic research portfolio, not a redistribution of third-party datasets. Confirm the permissions and terms for WRDS, IMF, and any other source material before using or redistributing data. The accompanying thesis is the appropriate source for the full literature review, theory, tables, and discussion.

## Licence and citation

Code in this repository is available under the [MIT License](LICENSE). See [CITATION.cff](CITATION.cff) for citation guidance.
