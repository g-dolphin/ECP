#!/usr/bin/env bash
set -euo pipefail

python -m src.download_edgar
python -m src.prep_boundaries
python -m src.aggregate_adm1
python -m src.export_inventory
