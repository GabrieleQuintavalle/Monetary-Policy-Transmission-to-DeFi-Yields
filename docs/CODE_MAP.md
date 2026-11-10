# Code-to-thesis map

Table and figure numbers refer to the submitted PDF. Original cell indexes are zero-based. Every selection and exact source diff is recorded in [PROVENANCE.json](PROVENANCE.json).

| Thesis result | Selected notebook | Original source / cells | Evidence and status |
| --- | --- | --- | --- |
| Table 3.4: Curve regressions | `01_yield_regressions` | `AAVE v2/REGRESSIONDAUSARE.ipynb`, 5 | Saved coefficients, z statistics, N=1,715 and adjusted R² match |
| Table 5.3: Curve VIF | `01_yield_regressions` | Same source, 6 | Saved VIFs match |
| Table 3.6: lending regressions | `01_yield_regressions` | Same source, 1 | **Recovered benchmark configuration:** replace `future 2y` with `3m ir`; the rerun reproduces all printed coefficients, z statistics, N and adjusted R² |
| Table 5.4: lending VIF | `01_yield_regressions` | Same source, 3 | Historical saved VIFs match the submitted table, but use the source's `future 2y` configuration. Rerun VIFs after restoring `3m ir` differ. The historical output is retained and explicitly identified |
| Table 3.1: Chow tests | `02_structural_breaks` | `AAVE v2/chow test.ipynb`, 0 | Saved F=2.81 and 6.96 and p-values match; the separate performance-metric calculation was not found |
| Table 3.3 and Figure 3.2 | `03_curve_local_projections` | `AAVE v2/LOCAL PROJECTIONS FINALE.ipynb`, 1–2 | Exact saved h=7 coefficient 0.025362 and p=0.000109; without-controls coefficient 0.023882. Submitted PNG also matches the archived image file byte for byte |
| Table 3.5: lending event study | `04_lending_event_study` | `AAVE v2/event(future2y_stable coin).ipynb`, 4 | Historical coefficients 0.0327 at T+7 and 0.0256 at T+18 and their p-values match. Imports/CSV loading recovered from cell 2; the function and model are retained |
| Figure 3.3 and Table 5.6 | `05_lending_local_projections_and_surprises` | `AAVE v2/gss eevnt.ipynb`, 2 | Submitted LP PNG matches the archived image byte for byte; saved target/path estimates match Table 5.6 |
| Tables 3.9–3.11: Curve Granger | `06_granger_by_regime` | `AAVE v2/granger stablecoin CLAUDE.ipynb`, 8 | Treasury F statistics 0.244, 3.952, 7.709 match; output filenames renamed to avoid collisions |
| Tables 3.12–3.14: lending Granger | `06_granger_by_regime` | Same source, 1 | Treasury F statistics 0.326, 5.629, 4.572 match; output filenames renamed to avoid collisions |
| Tables 3.15–3.17: TVL Granger | `06_granger_by_regime` | Same source, 5, with regime driver recovered from 1/8 | **Recovered driver:** source cell 5 currently runs a full-sample variant while saved output contains three regimes. Use the period loop from cells 1/8 with cell 5's functions, TVL transformation and variable order. F=1.407, 1.463, 8.223 match |
| Table 3.18: combined Granger table | `06_granger_by_regime` | Same sources as above | Synthesizes the three verified regime analyses |
| Table 5.5: daily TVL event study | `07_tvl_event_study` | `AAVE v2/TVL DELLA TESI CON SENSITIVITA.ipynb`, 4 | Saved daily coefficients and p-values match the displayed subset. Original cell includes -10 to +20; thesis displays -2 to +20 |
| Table 3.8 and Figures 3.4, 5.1–5.2 | `08_tvl_price_adjustment_and_placebo` | `AAVE v2/Tvl  CLAUDE.ipynb`, 4–5 | T+2 nominal -20.7156 and adjusted -32.7266 round to submitted values; three submitted diagnostic/interpretation PNGs are identical to archived files |
| Table 3.7 and Figure 5.3 | `08_tvl_price_adjustment_and_placebo` | Same source, 6, depends on 4 | Saved empirical p-values 0.046/0.064 and submitted PNG preserved; Monte Carlo seed was not recorded, so new p-values vary |

## Boundaries of recovery

- **Table 3.2 and Figure 3.1:** related Curve surprise/event-study variants exist, but no supplied source/output pair establishes the exact submitted specification. For example, `gss eevnt.ipynb` cell 0 currently has no controls and yields different significance from Table 3.2. This cell was excluded rather than presented as the exact thesis code. The submitted Figure 3.1 is kept in `results/thesis_figures/`.
- **Figures 1.1–1.2 and 2.1:** `comparazione.pdf`, `correlazione.pdf`, and `ammcurves.pdf` are kept as submitted; their exact generator code was not located.
- **Table 3.1 performance metrics, Table 3.19 aggregate comparison, and Appendix descriptive statistics:** no exact standalone source was established. Relevant inputs and verified neighbouring analyses are present, but no new calculation is labelled historical code.
- **Data collection:** the CSVs read by the selected calculations are archived inputs; they are not distributed in this repository (see the README, section "Data availability"). The original SQL queries and full raw-to-final construction of the lending indices were not recovered. The data-download notebook in the main archive primarily downloads Ethena/sUSDe, which is outside the submitted comparison. A separate Curve-folder downloader references a Dune query, but its exported columns are gas statistics; it does not establish the complete historical acquisition pipeline and is not included.

## Preservation choices

The submitted PDF and submitted figures are byte-identical copies. The input snapshots were byte-identical to the archived originals when verified, but they are not distributed in this repository. Empty cells, exploratory duplicates and checkpoint folders are omitted. A small first cell locates the bundle and directs new outputs into `results/rerun/`; CSV filenames in source cells become explicit bundle-relative paths.

Other than the three recoveries identified above, there are no changes to model formulas, controls, annualisation, filters, regime boundaries, date parsers, lag selection, or inferential settings. Granger inputs retain the source's `dayfirst=False` behaviour; changing it alters the reported results, so it has deliberately not been changed. Source comparisons in PROVENANCE.json make every edit reviewable.

Historical printed outputs are evidence of the original execution state, not proof that every current cell was last executed with its current settings. In particular, the archived regression output for source cell 1 remains the future-2y variant; the restored lending output is in the delivered notebook and fresh execution results.
