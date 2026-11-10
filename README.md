# Monetary Policy Transmission to DeFi Yields

Code companion to the submitted thesis by Gabriele Erminio Quintavalle and Luca Paul Beitone, Nova School of Business and Economics.

This repository contains eight selected notebooks, the submitted thesis PDF, and the ten figures actually included in the thesis. Selection was based on saved numeric outputs, matching thesis tables, and file hashes. Experimental cells, duplicate checkpoints, unrelated Ethena/sUSDe work, and credentials were excluded.

**The input datasets are not included** (see [Data availability](#data-availability)). The thesis PDF is unchanged. Notebook calculations retain the historical research choices. Recovered settings and cell dependencies are explicitly documented in [CODE_MAP.md](docs/CODE_MAP.md); they are not presented as untouched original code.

## Research overview

This thesis investigates how US monetary policy shocks are transmitted to decentralized finance (DeFi) markets, focusing on the interaction between liquidity provision, lending rates and total value locked (TVL).

Using market and on-chain data covering January 2021 to September 2025, the analysis examines three major DeFi protocols: Curve Finance, Aave and Compound.

The empirical framework combines FOMC event studies, local projections, VAR analysis and Granger causality tests to investigate the timing, magnitude and persistence of monetary policy transmission across different DeFi market segments.

## Start here

1. Read `thesis/Thesis Nova 2026 Luca Paul Beitone.pdf`.
2. Use [CODE_MAP.md](docs/CODE_MAP.md) to locate the notebook behind each result.
3. Open `notebooks/` in JupyterLab. The delivered notebooks have recorded outputs, so their results can be inspected without rerunning anything.

For an overview of the regression, event-study and VAR work, see notebooks 01, 03, 04 and 06. Notebook 08 contains the TVL diagnostics and the more time-consuming placebo simulation.

## Data availability

The input datasets used in the thesis are **not distributed** in this repository, because they combine third-party sources whose redistribution terms are not fully documented. The `data/` folder is intentionally empty.

- [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) describes each input file, its columns and the notebooks that use it.
- [docs/DATA_CHECKSUMS.csv](docs/DATA_CHECKSUMS.csv) lists SHA-256 checksums of the original files, so that anyone holding a copy can verify it.
- The original data-construction pipeline (SQL queries and raw-to-final construction of the panels) could not be recovered, see [CODE_MAP.md](docs/CODE_MAP.md). The results therefore **cannot be fully reproduced from public sources alone**.

Third-party data remain subject to the terms of their respective owners. Anyone reusing or redistributing them should check the original providers' terms.

## Running the code

The notebooks read their inputs from `data/` (see the file names in the data dictionary). Without those files they cannot be run, but the recorded outputs in `notebooks/` and the archived results in `results/` remain available for inspection.

If you have files with the same names and structure:

```
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run_analysis.py --quick
```

On Windows, activate the environment with `.venv\Scripts\activate`.

`--quick` runs all deterministic cells and skips the 1,000-iteration simulation. To run everything: `python run_analysis.py`. To run one notebook, for example the Curve local projections: `python run_analysis.py --only 03`.

Fresh outputs are written to `results/rerun/<notebook-name>/`. To refresh the displayed outputs in `notebooks/` as well, add `--update-notebooks`.

## Folder contents

| Location | Contents |
| --- | --- |
| `thesis/` | Submitted thesis PDF |
| `notebooks/` | Selected, labelled analysis cells |
| `data/` | Empty: input datasets are not distributed |
| `results/thesis_figures/` | The ten figures included in the submitted document, unchanged |
| `results/archived_outputs/` | Historical text outputs recovered from selected original cells |
| `results/rerun/` | Calculations and execution logs from a verification run; separate from historical evidence |
| `docs/` | Code-to-thesis mapping, data dictionary, data checksums, provenance and verification |

## Coverage and historical outputs

Most regression, local-projection, lending-surprise and Granger results were located and verified. The complete historical code for every submitted result was not present in the supplied archive. In particular, the exact Curve surprise/pass-through comparison in Table 3.2, the introductory chart generators, the AMM illustration, and the complete original data-collection pipeline could not be established. Their submitted figures are preserved when they occur in the PDF. They are not replaced with newly invented code.

The original placebo simulation has no recorded random seed. The archived p-values and submitted image are preserved; a new 1,000-iteration simulation can yield different empirical p-values. Original source and saved output can also reflect different notebook states. [CODE_MAP.md](docs/CODE_MAP.md) identifies these cases, including the recovered lending specification and TVL regime driver.

See [VERIFICATION.md](docs/VERIFICATION.md) for the verification results (obtained with input files that are no longer distributed). This package preserves the submitted work; it does not revise the thesis's economic interpretations or change the original date-parsing and model choices.

## Licensing

No open-source license has been granted for this repository yet. Unless a license file is added, all rights are reserved by the authors. The thesis PDF and figures are the authors' work and are provided for reading and reference. Third-party data and series mentioned in this repository remain subject to their own terms.
