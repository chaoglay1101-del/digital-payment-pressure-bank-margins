# Digital Payment Pressure and Bank Net Fee Margins

**Research portfolio | Undergraduate accounting and finance project | ASEAN-5 bank panel**

This project investigates whether the growth of digital payment activity is associated with banks' net fee margins. It combines bank-level financial data with a country-year digital payment measure, then uses panel regressions to separate the relationship from persistent differences between banks and common changes over time.

> **Research question:** Is digital payment pressure associated with bank net fee margins in Indonesia, Malaysia, the Philippines, Singapore, and Thailand?

## Why this project matters

Digital payments may change how banks earn fee income. They can create new transaction opportunities, but they can also increase competition and reduce the fees earned from traditional payment services. This project tests that tension with an ASEAN-5 bank panel rather than assuming that digitalisation has an automatically positive effect.

## Portfolio highlights

- Built a reproducible data pipeline from bank-panel data and an IMF Financial Access Survey indicator.
- Standardised bank identifiers, constructed financial ratios, merged country-year data, and checked unmatched observations and currency conversion.
- Estimated bank and year fixed-effects models with bank-clustered standard errors.
- Added log, interaction, nonlinear, and country-sub-sample specifications to examine whether the baseline relationship changes across model choices.
- Documented data decisions and validation checks so that the empirical result can be assessed rather than treated as a black box.

## Main findings

The final regression sample contains **344 observations from 39 banks between 2014 and 2022**. Across the main specifications, the coefficient on digital payment pressure is negative, but the evidence is not consistently statistically significant. The log specification also produces a negative estimate, while the country sub-samples point to heterogeneous relationships rather than one uniform ASEAN-wide pattern.

These results should be read as **conditional associations, not causal proof**. The sample, measurement of digital payment pressure, omitted variables, and the country-level nature of the main explanatory variable all limit causal interpretation.

## Research design

1. **Define the outcome:** net fee margin is the bank-level dependent variable.
2. **Construct the explanatory measure:** identify and extract a country-year digital payment indicator from the IMF Financial Access Survey workflow.
3. **Build the panel:** combine the country-year measure with bank-year observations and calculate controls for capital adequacy, size, credit risk, interest expense, and deposits.
4. **Estimate the models:** use bank fixed effects, year fixed effects, clustered standard errors, and 1st/99th percentile winsorisation.
5. **Test robustness:** compare raw scaled and log measures, large-bank interactions, a centred nonlinear specification, and country sub-samples.

The full research-stage-to-file mapping is available in [docs/research-process.md](docs/research-process.md).

## Run the public example

The restricted thesis datasets are not included in this repository. To demonstrate the modelling workflow without exposing those files, the repository includes a small deterministic synthetic panel:

```powershell
python examples/run_example.py
```

The command creates [examples/example_panel.csv](examples/example_panel.csv) and estimates a bank and year fixed-effects model with bank-clustered standard errors. The generated coefficient is only a software demonstration; it is not part of the thesis results.

## Selected results

| Specification | Digital payment coefficient | Observations | Interpretation |
| --- | ---: | ---: | --- |
| Main model, scaled measure | -0.000292* | 344 | Negative association; marginal statistical evidence |
| Main model with controls | -0.000264 | 344 | Negative association; not statistically significant |
| Full controls model | -0.000208 | 344 | Negative association; not statistically significant |
| Log baseline model | -0.010171** | 344 | Negative association under the log specification |
| Nonlinear model | -0.010829** | 344 | Negative linear term; squared term not significant |

`* p < 0.10`, `** p < 0.05`. Estimates are reported here to make the portfolio transparent; consult the generated result tables for standard errors and the full specification.

## Repository guide

| Research stage | File |
| --- | --- |
| Panel cleaning and financial ratios | [process_panel_data.py](process_panel_data.py) |
| FAS indicator discovery | [search_fas_indicators.py](search_fas_indicators.py) |
| Digital payment extraction | [extract_digital_payment_pressure.py](extract_digital_payment_pressure.py) |
| Panel merge | [merge_digital_pressure_to_bank_panel.py](merge_digital_pressure_to_bank_panel.py) |
| Main and advanced regressions | [512版迴歸/run_regressions_FINAL_clean.py](512版迴歸/run_regressions_FINAL_clean.py) |
| Country sub-sample robustness | [512版迴歸/run_robustness_country_subsamples.py](512版迴歸/run_robustness_country_subsamples.py) |
| Research process and decisions | [docs/research-process.md](docs/research-process.md) |
| Public synthetic-data demonstration | [examples/run_example.py](examples/run_example.py) |

## Reproduction notes

The scripts use project-root-relative paths. The intended workflow is:

```text
clean bank panel -> identify/extract indicator -> merge and validate -> run main regressions -> run robustness checks
```

The full WRDS/IMF source files, derived datasets, course submissions, reflective logs, and local environment files are excluded from the public release. Before publishing this repository, confirm redistribution permissions and add a small synthetic example if visitors need to execute the pipeline without restricted data.

## Tools

Python 3.14+, pandas, NumPy, linearmodels, statsmodels, matplotlib, openpyxl, and python-docx. Package metadata is recorded in [pyproject.toml](pyproject.toml).

## Academic and data note

This repository is an academic research portfolio, not a redistribution of third-party datasets. The reported results are a concise portfolio summary of the accompanying thesis; the thesis remains the appropriate source for the full literature review, theory, tables, and discussion.
