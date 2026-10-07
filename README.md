# Digital Payment Pressure and Bank Net Fee Margins

**Research portfolio | Undergraduate accounting and finance project | ASEAN-3 bank panel**

[繁體中文版](README.zh-TW.md)

[LinkedIn](https://www.linkedin.com/in/yu-chen-chao/)

This project studies whether digital-payment activity is associated with banks' net fee margins in **Indonesia, Malaysia, and Thailand**. It combines bank-level financial data with an IMF Financial Access Survey (FAS) country-year measure, then estimates fixed-effects panel regressions to distinguish the relationship from persistent bank differences and common time trends.

> **Research question:** Is digital payment pressure associated with bank net fee margins in Indonesia, Malaysia, and Thailand?

## Why it matters

Digital payments can create transaction opportunities for banks while also increasing competition for traditional payment fees. Rather than assume one outcome, this project tests the association in an ASEAN-3 bank panel.

## Key findings

The final thesis sample contains **344 observations from 39 banks between 2014 and 2022**. The outcome is the proxy for net fee and commission income: Compustat Global total non-interest income divided by total assets, which is the closest consistently available series across the three markets and also contains trading and other non-interest revenue.

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
| Size interaction model | -0.006507 | 344 | Large Bank dummy and interaction are not significant |
| Nonlinear model | -0.010829** | 344 | Negative linear term; squared term is not significant |

`* p < 0.10`, `** p < 0.05`.

### Robustness highlights

| Diagnostic | Estimate | Interpretation |
| --- | --- | --- |
| Driscoll-Kraay SE (Model 4) | -0.0102, SE 0.0035, p = 0.004 | Still significant when cross-sectional dependence is allowed |
| Mundlak within-country | -0.0049, SE 0.0079, p = 0.53 | No within-country association |
| Excluding 2020 | -0.008006, SE 0.004941, p = 0.106 | Similar size, less precise |
| One-year lag | -0.015901*, SE 0.008475, p = 0.062 | Larger and negative; eases the reverse-causality concern |

## Research design

1. Construct bank-level net fee margins and financial controls from the restricted bank panel.
2. Identify IMF FAS indicator `IMF_FAS_FCMIBT`, measured as mobile and internet banking transactions as a percentage of GDP (`PT_GDP`).
3. Merge the country-year measure with bank-year observations.
4. Estimate bank and year fixed-effects models with bank-clustered standard errors and 1st/99th percentile winsorisation.
5. Assess log, interaction, nonlinear, and country-subsample specifications.

The detailed decision trail is in [docs/research-process.md](docs/research-process.md). For a GitHub-readable account of the research question, design, results, limitations, and data-access boundaries, see the [public research report](docs/public-research-report.md).

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

More public research documentation:

- [Full public research report](docs/public-research-report.md)
- [Variable definitions](docs/variable-definitions.md)
- [Methodology appendix](docs/methodology-appendix.md)
- [References](docs/references.md)
- [Research design diagram](docs/research-design.svg)

The intended restricted-data workflow is:

```text
02_Data/01_Raw -> prepare bank panel -> download/discover/extract IMF indicator
-> merge panel -> run main regressions -> run country robustness checks
```

## Methods and tools

Python 3.14+, pandas, NumPy, linearmodels, statsmodels, matplotlib, openpyxl, and python-docx. Dependency metadata and reproducible environment resolution are in [pyproject.toml](pyproject.toml) and [uv.lock](uv.lock).

## Academic and data note

This is an academic research portfolio, not a redistribution of third-party datasets. Confirm the permissions and terms for WRDS, IMF, and any other source material before using or redistributing data. The accompanying [public research report](docs/public-research-report.md) provides the full public account of the study's design, results, and limitations. It does not include the restricted datasets, course-submission versions, or other private materials.

## Licence and citation

Code in this repository is available under the [MIT License](LICENSE). See [CITATION.cff](CITATION.cff) for citation guidance.
