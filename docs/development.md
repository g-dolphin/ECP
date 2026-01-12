# Development

## Tooling

- Python package utilities live in `_code/compilation/_utils/dep_ecp` and are exposed via `pyproject.toml`.
- R scripts handle portions of the industry matching pipeline under `_code/compilation/ecp/industry`.
- Quarto powers report rendering in `_code/reporting/reports`.

## Common commands

Generate charts:

```bash
python _code/reporting/charts/generate_charts.py
```

Render the report (HTML):

```bash
quarto _code/reporting/reports/report.qmd --to html --output wcpd_report.html
```

Render the report (PDF):

```bash
quarto render _code/reporting/reports/report.qmd --to pdf --output wcpd_report.pdf
```

## Notes

- The Makefile references absolute paths; adjust `SCRIPTS_DIR` and `OUTPUT_DIR` if your local clone differs.
- Some compilation notebooks and scripts assume local availability of the `_raw` datasets.
