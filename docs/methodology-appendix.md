# Methodology Appendix

This appendix records the public methodological design. It is intended to make the workflow inspectable without distributing restricted inputs or row-level outputs.

## 1. Data workflow

```text
Restricted bank panel                  IMF FAS public source
        │                                      │
        ├─ bank filtering and variables       ├─ indicator discovery
        │                                      └─ country-year extraction
        └──────────────┬───────────────────────┘
                       │
             country-year panel merge
                       │
          common analysis sample and cleaning
                       │
         fixed-effects association estimates
```

The public code separates these stages:

- [Prepare the bank panel](../src/data/prepare_bank_panel.py)
- [Download IMF FAS](../src/data/download_imf_fas.py)
- [Discover candidate indicators](../src/data/discover_fas_indicator.py)
- [Extract digital-payment pressure](../src/data/extract_digital_payment_pressure.py)
- [Merge the panels](../src/data/merge_bank_panel.py)
- [Estimate main specifications](../src/analysis/run_main_regressions.py)
- [Estimate country subsamples](../src/analysis/run_country_subsamples.py)

## 2. Main panel specification

A generic two-way fixed-effects specification is:

\[
NFM_{it} = \beta DPP_{ct} + \boldsymbol{\gamma}'\mathbf{X}_{it}
+ \alpha_i + \lambda_t + \varepsilon_{it},
\]

where:

- \(NFM_{it}\) is bank \(i\)'s net fee margin in year \(t\);
- \(DPP_{ct}\) is the digital-payment-pressure measure for country \(c\) and year \(t\);
- \(\mathbf{X}_{it}\) is a vector of bank-level controls;
- \(\alpha_i\) is a bank fixed effect;
- \(\lambda_t\) is a year fixed effect; and
- \(\varepsilon_{it}\) is the residual.

The coefficient \(\beta\) is interpreted as a conditional association within the stated model. It is not automatically a causal effect because digital-payment development may be correlated with regulation, infrastructure, market structure, macroeconomic conditions, and other omitted factors.

## 3. Variable transformations

The workflow evaluates several forms of the explanatory measure:

- a scaled specification, reported as `DPP_10pct_GDP`;
- a logarithmic specification, reported as `Log_Digital_Payment_Pressure`;
- an interaction specification involving `Large_Bank`; and
- a nonlinear specification involving a centred log measure and its square.

For a nonlinear specification, the conceptual form is:

\[
NFM_{it} = \beta_1 DPP^c_{ct} + \beta_2 (DPP^c_{ct})^2
+ \boldsymbol{\gamma}'\mathbf{X}_{it} + \alpha_i + \lambda_t + \varepsilon_{it},
\]

where \(DPP^c_{ct}\) is the log measure centred around its sample mean before squaring. Centreing helps reduce mechanical correlation between the linear and squared terms; it does not solve omitted-variable or identification problems.

## 4. Cleaning and estimation choices

### Complete-case sample

The main workflow forms a common estimation sample using the required outcome, explanatory, and control variables before estimating the reported specifications. This makes model comparisons easier to interpret, but it can reduce the available sample if variables are missing.

### Winsorisation

Continuous variables are winsorised at the 1st and 99th percentiles within the analysis sample. This limits the influence of extreme observations; it does not make the observations representative or remove all measurement concerns.

### Standard errors

The main specifications use standard errors clustered at the bank level to account for dependence within bank histories. Country-level variation in the explanatory measure remains an important limitation: bank clustering alone does not create additional independent country-level observations.

### Country subsamples

Country-level robustness checks retain bank fixed effects. Year effects are excluded in the single-country specification because a country-year explanatory variable can be absorbed by year indicators when there is only one country in the subsample. This check is diagnostic and should not be interpreted as a replacement for a stronger causal design.

## 5. Reported specifications

The public report summarises the following model families:

1. scaled digital-payment pressure;
2. scaled pressure with additional financial controls;
3. a full-controls specification;
4. a logarithmic baseline specification;
5. an interaction specification for bank size;
6. a centred nonlinear specification; and
7. country-subsample robustness specifications.

The headline coefficients and interpretations are reported in the [public research report](public-research-report.md). The exact thesis estimates cannot be regenerated from a public clone because the underlying bank panel and derived datasets are restricted.

## 6. What this appendix does not provide

This public appendix deliberately excludes:

- raw bank observations;
- bank names or identifiers;
- restricted WRDS exports;
- complete derived panel files;
- private regression logs and submission documents;
- teacher feedback, grades, signatures, and course-only materials; and
- any output that could allow a reader to reconstruct the restricted dataset.

The public synthetic example demonstrates the general fixed-effects workflow, but it does not reproduce the thesis data or results:

```powershell
uv run python examples/run_example.py
uv run pytest
```
