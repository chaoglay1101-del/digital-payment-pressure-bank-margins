# Research Process

This page connects the repository files to the sequence of decisions in the research project.

## 1. Research design

The project studies the relationship between digital payment pressure and bank net fee margins in an ASEAN-5 panel. The research design identifies the outcome, the country-year digital-payment measure, bank-level controls, and fixed-effects specifications.

Supporting material is kept outside the public code surface because it contains course submissions, drafts, and research notes.

## 2. Bank panel construction

`process_panel_data.py` reads the WRDS-style bank panel and the ASEAN-5 bank list. It filters observations by country, standardises bank names, retains the financial variables required by the study, handles selected missing values, and calculates ratios such as:

- liquidity ratio;
- loan-to-deposit ratio;
- capital adequacy proxy; and
- net fee margin.

The output is `Academic_Bank_Panel_Data_Cleaned.csv`, which is ignored from the public repository because it is a derived dataset.

## 3. Digital payment indicator

The indicator workflow is split into discovery and extraction:

- `search_fas_indicators.py` searches the IMF FAS wide-format file for candidate indicators.
- `get_fas_mobile_internet_banking_from_data360.py` retrieves the relevant data source.
- `extract_digital_payment_pressure.py` reshapes the selected country-year indicator into a mergeable table.

This separation makes the measurement decision inspectable: indicator discovery is distinct from the final extraction step.

## 4. Merge and validation

`merge_digital_pressure_to_bank_panel.py` joins the country-year digital-payment measure to the cleaned bank panel. `check_merge_problem.py` is used to investigate unmatched observations and key-format issues. `fx_conversion_validation_summary.csv` records currency-conversion checks used during data validation.

The merged panel is an intermediate research output and is excluded from the public repository.

## 5. Regression analysis

The main cleaned regression workflow is in `512版迴歸/run_regressions_FINAL_clean.py`. It prepares the estimation sample, constructs transformed digital-payment variables, estimates panel models, and writes the main and advanced result tables.

`advanced_regression_tests.py` contains additional nonlinear and interaction specifications. The older scripts in the root directory are retained as development history and should be labelled clearly before public release.

## 6. Robustness and reflection

`512版迴歸/run_robustness_country_subsamples.py` estimates country-level subsample models for Indonesia, Malaysia, and Thailand. The project also contains written reflection and feedback material, but those documents remain outside the public GitHub portfolio because they are course and submission records.

## 7. Public demonstration

The restricted-data pipeline and the public demonstration are intentionally separate. `examples/run_example.py` creates a deterministic synthetic bank panel and estimates a simplified version of the fixed-effects model. It is included so visitors can verify the Python and `linearmodels` workflow without access to WRDS or IMF source files. Its coefficient is not evidence for the thesis.

Run it from the repository root:

```powershell
python examples/run_example.py
```

## Public release checklist

- Remove or anonymise any bank-level identifiers that cannot be redistributed.
- Confirm WRDS, IMF, and university data-use permissions.
- Add a small synthetic dataset and a public example command if full reproducibility is required.
- Keep synthetic example results clearly separate from the thesis results.
- Replace local or personal filenames in documentation.
- Review the final GitHub file list before publishing.