# Verification performed on 6 November 2026

> **Note.** This verification was run on 6 November 2026 using the seven input CSVs. Those files are no longer distributed in this repository, because they combine third-party sources whose redistribution terms are not fully documented. The results below are therefore a historical record: they cannot be re-run from this repository alone. SHA-256 checksums of the original input files are listed in `DATA_CHECKSUMS.csv`.

All eight selected notebooks ran successfully using the input CSVs (not distributed here, see note above). The complete TVL placebo cell also finished its original 1,000 iterations. No input data, thesis PDF, or original source notebook was modified.

The deterministic and integrity checks passed **136/136**. The machine-readable results are in [verification_results.json](verification_results.json). Execution logs and exported numbers are in `results/rerun/`; notebook outputs are displayed in `notebooks/`.

## Representative reproduced results

| Result | Rerun value | Submitted value / comparison |
| --- | --- | --- |
| Curve full-model Treasury coefficient | 0.0029989818 | 0.0030 |
| Curve full-model adjusted R² | 0.1189026543 | 0.119 |
| Lending full-model Treasury coefficient, restored benchmark | 0.0027432684 | 0.0027 |
| Lending funding coefficient | 0.0755231509 | 0.0755 |
| Lending full-model adjusted R² | 0.3505616544 | 0.351 |
| Regression observations | 1,715 | 1,715 |
| Chow F, first / second break | 2.8081203 / 6.9595168 | 2.81 / 6.96 |
| Curve LP h=7, with controls | 0.0253624502; p=0.0001094196 | 0.025; p<0.001 |
| Curve LP h=7, without controls | 0.023882; p=0.004880 | 0.024; p=0.005 |
| Lending event study T+7 / T+18 | 0.0327 / 0.0256 | Same printed coefficients and p-values |
| Lending path surprise at h=3 | 0.0003046126; p=0.0315402401 | 0.0003; p=0.032 |
| Treasury → Curve Granger, three regimes | 0.244 / 3.952 / 7.709 | Same printed F statistics |
| Treasury → lending Granger, three regimes | 0.326 / 5.629 / 4.572 | Same printed F statistics |
| Treasury → adjusted TVL Granger, three regimes | 1.407 / 1.463 / 8.223 | Same printed F statistics |
| Daily TVL event study T+2 | -0.2081 | -0.2081 |
| TVL T+2 nominal / adjusted | -20.7155869 / -32.7265540 | -20.72 / -32.73 |

The checks also validate the individual source-cell hashes, all seven CSV copies, the submitted PDF, and all ten submitted figures. Notebook JSON was validated using nbformat. Selected code was checked for embedded credential assignments; none were included.

## Stochastic output

The archived TVL placebo output reports empirical p-values 0.046 and 0.064 at T+2. The verification rerun produced 0.054 and 0.050. This is a new random draw from the original 1,000-iteration simulation, not a replacement of the submitted results. No historical seed is recorded in the source. Both the archived output and the submitted figure remain available unchanged.

## Runtime

- Python 3.12.2
- NumPy 1.26.4
- pandas 2.2.2
- SciPy 1.13.1
- statsmodels 0.14.2
- Matplotlib 3.9.2
- tabulate 0.9.0
- nbformat 5.10.4 for notebook validation

The original date-parser behaviour and research specifications were preserved. The explicitly recovered configurations and source/output discrepancies are described in [CODE_MAP.md](CODE_MAP.md). These checks establish execution and the stated matches; they do not claim that every result in the submitted PDF has a fully recovered source.

## Portability

The runner, notebooks and data were copied to a separate folder under `/tmp`. Notebook 02 executed successfully there with the same numeric results, confirming that input paths do not depend on the original desktop location.
