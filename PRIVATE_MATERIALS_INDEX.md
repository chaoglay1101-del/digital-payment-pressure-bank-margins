# Private research materials index

This repository contains the public, reproducible code portfolio. Local course files, restricted data, assignment drafts, submission records, and graduate-application materials are organised separately and remain ignored by Git.

## Folders

| Folder | Contents |
| --- | --- |
| `00_Admin_and_Guidance/` | Module handbook, assignment remits, and research ethics documents. |
| `01_Literature/` | Source papers and citation/reference-management material. |
| `02_Data/01_Raw/` | Restricted or externally sourced inputs. Do not distribute without permission. |
| `02_Data/02_Reference_and_Templates/` | Data templates and indicator-discovery references. |
| `02_Data/03_Intermediate/` | Cleaned and merged research datasets. |
| `02_Data/04_Analysis_Output/` | Regression samples, tables, validation summaries, and robustness outputs. |
| `03_Methods_and_Instruments/` | Interview and research instruments. |
| `04_Course_Materials/` | Dated class slides, readings, exercises, and transcripts. |
| `05_Analysis_and_Working/` | Working notes, historical regression run files, drafts, and exploratory scripts. |
| `06_Submissions/` | Research-report and reflective-log submission histories. |
| `07_Graduate_Applications/` | Graduate-application documents and planning notes. |
| `08_Tools/` | Local software installers. |
| `09_Business_Analytics/` | Business Analytics coursework, data, Tableau workbooks, and related materials. |

## Naming rules

- Dated learning materials use `YYYY-MM-DD_topic_type.ext`.
- Data files use `scope_subject_processing-state.ext`, such as `ASEAN5_Bank_Panel_Cleaned.csv`.
- Citation-oriented source-paper filenames retain author and year information where available.
- Submission drafts and review files retain their version/date trail instead of being deleted.

## Reproducing the restricted workflow

The research scripts now expect local data in `02_Data/`. The intended sequence is:

```text
02_Data/01_Raw
  → 02_Data/03_Intermediate
  → 02_Data/04_Analysis_Output
```

The data and private-material folders remain excluded by `.gitignore`; code, documentation, tests, and the public synthetic example keep their existing repository locations.
