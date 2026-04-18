# Emissions-weighted Carbon Price

This site documents the structure, data sources, and processing pipeline used to produce the Emissions-weighted Carbon Price (ECP) dataset and its reporting outputs.

The ECP is an economy-wide average price on CO2 emissions, computed from sector-fuel data and aggregated with emissions weights. The methodology is described in Dolphin and Merkle (2024).

## Repository layout

| Area | Purpose |
| --- | --- |
| `_raw` | Primary inputs: pricing data, inventory metadata, exchange rates, and mapping files. |
| `_code/compilation` | Data compilation, matching, and ECP calculations (R, Python, notebooks). |
| `_code/reporting` | Chart generation and report assembly (Python, R, Quarto). |
| `_output` | Final datasets, figures, tables, and reports. |

## Build the docs

Install dependencies:

```bash
pip install mkdocs pymdown-extensions
```

Serve locally:

```bash
mkdocs serve
```

Build HTML:

```bash
mkdocs build
```

## Related materials

- Dataset paper: Dolphin, G., Merkle, M. (2024). Emissions-weighted Carbon Price: Source and Methods. Scientific Data.
- Pricing data repository: https://github.com/gd1989/WorldCarbonPricingDatabase
- Public/private repository boundary: see `Public Scope`.
