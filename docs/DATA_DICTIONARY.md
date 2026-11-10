# Input data (not distributed)

**The input CSV files are not included in this repository.** They combine third-party sources whose redistribution terms are not fully documented, so they have been removed. SHA-256 checksums of the original files are listed in [DATA_CHECKSUMS.csv](DATA_CHECKSUMS.csv), so that anyone who obtains files claiming to be the originals can check them.

The seven files below were historical snapshots read by the selected notebooks. Some included a UTF-8 BOM and trailing empty spreadsheet rows; the original notebook loaders and missing-value handling are retained. Dates are mainly `DD/MM/YY`, except the monthly Fed file. Each notebook keeps its original date-parsing behaviour to preserve the historical output.

To run a notebook, place a file with the same name and column structure in the `data/` folder (see the columns table below).

| File | Role | Used by | Source |
| --- | --- | --- | --- |
| `aavegas.csv` | Daily protocol returns, Treasury benchmark and crypto/macro controls | 01, 04 | Panel built by the thesis authors from several sources; original source records not preserved |
| `aavenew.csv` | Expanded daily protocol/market panel with aggregate TVL | 03 | Panel built by the thesis authors from several sources; original source records not preserved |
| `aavebtc.csv` | Daily master panel including BTC return and volatility, ETH price and TVL variables; 1,715 rows from the 2021-2025 sample | 02, 05, 06 | Panel built by the thesis authors from several sources; original source records not preserved |
| `aavetvl.csv` | TVL panel, ETH price, stored Fed funds series and controls | 07, 08 | Panel built by the thesis authors from several sources; original source records not preserved |
| `ABJ-2024.csv` | FOMC dates and monetary surprise factors; 234 historical events through May 2024 | 03-05, 07-08 | Third-party research dataset, not produced by the thesis authors. The original authors' citation and terms of use apply |
| `btc_filtered.csv` | BTC daily return and volatility panel used to join regression controls | 01 | Panel built by the thesis authors; original source records not preserved |
| `FEDFUNDS.csv` | Monthly `FEDFUNDS` series, percentage units; used by the conditional fallback loader in notebook 08 | 08 fallback | Federal Reserve Bank of St. Louis, FRED, series FEDFUNDS |

The overlap between panel files is intentional: the selected historical notebooks read different snapshots. Consolidating them into a newly cleaned master panel would change provenance and potentially sample selection.

## Columns referenced in analyses

| Column | Meaning / stored convention |
| --- | --- |
| `date`, `Date` | Historical observation date; parsing is specified in each source cell |
| `3pool` | Stored daily Curve liquidity-provision yield/return in decimal units; annualised APY figures are distinct from this stored series |
| `stablecoin` | Stored daily aggregate lending yield/return in decimal units |
| `usdc`, `usdt` | Stored daily stablecoin lending components |
| `3m ir` | Three-month Treasury rate in decimal annual-rate units |
| `future 2y` | Archived two-year market series; present in the historical panels but not the restored lending benchmark |
| `ETF 1-3m` | Archived short-Treasury ETF return series |
| `ethperpetual` | Stored ETH perpetual funding series |
| `gas_fees` | Ethereum gas-price control in the historical panel |
| `gas%` | Stored gas change series used in TVL event studies |
| `S&P 500`, `VIX` | Stored market-control series; retain archived transformations |
| `sum of tvl` | Aggregate TVL level in USD as supplied in the final input panel |
| `tvl%` | Stored TVL change; notebook 08 also computes its own percentage changes from the level |
| `FEDFUNDS` | Fed funds series; scripts conditionally divide by 100 if values are in percentage units |
| `eth`, `eth%` | ETH price level and stored change |
| `btc_return`, `volatility_btc` | BTC return and volatility controls |
| `GSS_target`, `GSS_path`, `NS` | Archived surprise factors from the supplied ABJ file; selected code uses target and path |

The full original SQL, protocol-pool weighting history and raw-to-final transformation pipeline were not present. Therefore, this dictionary describes the analysis inputs and their code usage; it does not certify unrecorded upstream transformations. No winsorisation, rescaling or new cleaning was applied to the archived CSVs.
