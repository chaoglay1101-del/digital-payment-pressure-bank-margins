# Variable Definitions

This page documents the public conceptual definitions used in the research report. It intentionally excludes bank identifiers, raw observations, restricted derived datasets, and any values that could reveal the underlying private panel.

## Observation and data levels

| Level | Meaning | Role in the study |
| --- | --- | --- |
| Bank-year | One bank observed in one financial year | Main unit of the outcome and bank controls |
| Country-year | One country observed in one year | Level of the digital-payment-pressure measure |
| Bank fixed effect | A time-invariant bank component | Controls for persistent differences between banks |
| Year fixed effect | A period component shared by the panel | Controls for common time shocks |

The final public description covers 39 banks and 344 bank-year observations in Indonesia, Malaysia, and Thailand between 2014 and 2022.

## Main variables

| Variable | Conceptual definition | Level | Expected interpretation | Public-data status |
| --- | --- | --- | --- | --- |
| `Net_Fee_Margin` | Net fee income relative to total assets | Bank-year | A bank-level measure of fee-based income relative to its asset base | Constructed from restricted bank financial data |
| `Digital_Payment_Pressure` | Mobile and internet banking transactions as a percentage of GDP | Country-year | A broad measure of digital-payment activity relative to the economy | Selected from IMF FAS; source is public, generated output is not committed |
| `Log_Digital_Payment_Pressure` | Log-transformed digital-payment-pressure measure | Country-year | Reduces scale sensitivity and represents a proportional-style specification | Derived in the restricted analysis workflow |
| `DPP_10pct_GDP` | A rescaled form of the digital-payment measure | Country-year | Makes small coefficient magnitudes easier to read | Derived in the restricted analysis workflow |
| `Size_USD` | Bank size expressed using the analysis currency convention | Bank-year | Controls for scale differences between banks | Constructed from restricted bank financial data |
| `Capital_Adequacy_Proxy` | Equity relative to total assets | Bank-year | A simple balance-sheet capitalisation proxy | Constructed from restricted bank financial data |
| `Credit_Risk` | Credit-risk measure based on the bank financial variables available to the project | Bank-year | Controls for differences in asset-quality exposure | Constructed from restricted bank financial data |
| `Interest_Expense_Ratio` | Interest expense relative to the selected bank scale denominator | Bank-year | Controls for funding-cost differences | Constructed from restricted bank financial data |
| `Deposit_Ratio` | Deposit-related balance-sheet measure relative to the selected bank scale denominator | Bank-year | Controls for funding structure | Constructed from restricted bank financial data |
| `Large_Bank` | Indicator based on the analysis sample's bank-size classification | Bank-year | Supports a size-heterogeneity specification | Derived from restricted analysis data |
| `Digital_x_LargeBank` | Interaction between digital-payment pressure and the size indicator | Bank-year | Tests whether the association differs by bank size | Derived in the restricted analysis workflow |

## IMF FAS indicator

The selected source indicator is `IMF_FAS_FCMIBT`, used with unit `PT_GDP`. In the project documentation it represents mobile and internet banking transactions as a percentage of GDP. The public workflow makes the measurement choice inspectable through:

- [IMF FAS download script](../src/data/download_imf_fas.py)
- [Indicator discovery script](../src/data/discover_fas_indicator.py)
- [Digital-payment extraction script](../src/data/extract_digital_payment_pressure.py)

The source's availability, indicator definitions, and reuse terms can change. Researchers should consult the current [IMF Financial Access Survey source](https://data360.worldbank.org/en/dataset/IMF_FAS) before reproducing or extending the measure.

## Construction principles

1. **Keep source levels distinct.** Bank-year financial variables are not treated as if they were country-level indicators, and the country-year payment measure is not described as a bank-specific observation.
2. **Make transformations explicit.** Log and rescaled measures are transformations of the selected payment indicator, not new independent data sources.
3. **Control extreme values transparently.** The main workflow winsorises continuous variables at the 1st and 99th percentiles within the analysis sample.
4. **Avoid causal overstatement.** A coefficient describes a conditional association under a model specification; it does not by itself identify a causal effect.
5. **Respect restricted data.** No raw values, bank names, row-level exports, or complete derived datasets are published here.

## Interpretation limits

The digital-payment measure varies at the country-year level, while the outcome is measured at the bank-year level. This limits the within-country variation available for interpretation. The final sample also covers only three countries, and the aggregated net fee margin does not separate payments, cards, merchant services, wealth management, or other non-interest-income components.
