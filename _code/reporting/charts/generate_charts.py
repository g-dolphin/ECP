from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

# --------------------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------------------

# This file lives in: ECP/_code/reporting/charts/generate_charts.py
CHARTS_DIR = Path(__file__).resolve().parent
# repo root assumed to be two levels up: ECP/
REPO_ROOT = CHARTS_DIR.parents[2]

OUTPUT_ROOT = REPO_ROOT / "_output" / "_figures"
PLOTS_DIR = OUTPUT_ROOT / "plots"
DATA_DIR = OUTPUT_ROOT / "dataFig"
REGISTRY_PATH = OUTPUT_ROOT / "chart_registry.json"

PLOTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------------------
# Imports from local plotting modules
# (make sure these files contain the refactored functions as discussed)
# --------------------------------------------------------------------------------------

from proc_carbonPrices import prepare_carbon_price_data
from plots_carbonPrices import plot_minMax
from plots_coverage import coverage_plots
from plots_world_sectors import plot_world_sectors
from plots_ets_tax_jur import plot_selected_jurisdictions
from plots_subnat_stacked import plot_filtered_stacked_bar
from plots_national_stacked import plot_stacked_national_bar

from plots_cp_gdp import plot_cp_gdp
from plots_cp_ts import plot_cp_ts_jurisdictions, plot_cp_ts_world_sectors
from plots_cp_regional import plot_cp_regional
from plots_ccost_gdp import plot_ccost_gdp
from plots_coverage_heatmaps import plot_coverage_heatmap

# --------------------------------------------------------------------------------------
# Static lists used in several charts
# --------------------------------------------------------------------------------------

CANADIAN_PROVINCES = [
    "Alberta",
    "British Columbia",
    "Manitoba",
    "New Brunswick",
    "Newfoundland and Labrador",
    "Nova Scotia",
    "Ontario",
    "Prince Edward Island",
    "Quebec",
    "Saskatchewan",
]

US_STATES = [
    "California",
    "Connecticut",
    "Delaware",
    "Maine",
    "Maryland",
    "Massachusetts",
    "New Hampshire",
    "New Jersey",
    "New York",
    "Rhode Island",
    "Vermont",
    "Virginia",
    "Washington",
]

CHINA_PROVINCES = [
    "Beijing",
    "Chongqing",
    "Fujian",
    "Guangdong",
    "Hubei",
    "Shanghai",
    "Shenzhen",
    "Tianjin",
]

# Sector names reused for TS and bar charts
WORLD_SECTOR_MAP = {
    "1A1A1": "Electricity Generation",
    "1A1C": "Other Energy Industries",
    "1A2A": "Iron and Steel",
    "1A2B": "Non-Ferrous Metals",
    "1A2C": "Chemicals",
    "1A2D": "Pulp, Paper, Print",
    # "1A2E": "Food Processing",
    "1A2F": "Non-Metallic Minerals",
    # "1A2G": "Transport Equipment",
    "1A2H": "Machinery",
    "1A2J": "Mining and Quarrying",
    "1A3A1": "International Aviation",
    "1A3B": "Road Transport",
    "1A4A": "Buildings - Commercial and Institutional",
    "1A4B": "Buildings - Residential",
    "1A4C": "Agriculture, Forestry, Fishing",
}

# --------------------------------------------------------------------------------------
# Registry data structure
# --------------------------------------------------------------------------------------

@dataclass
class ChartRun:
    id: str
    title: str
    module: str
    function: str
    # paths are stored relative to OUTPUT_ROOT
    plot_file: Optional[str]
    data_file: Optional[str]
    params: Dict[str, Any]


# --------------------------------------------------------------------------------------
# Existing chart runners
# --------------------------------------------------------------------------------------

def run_carbon_price_minmax() -> ChartRun:
    """
    Max & average carbon price by jurisdiction (min/max bar chart).
    Uses:
      - proc_carbonPrices.prepare_carbon_price_data(data_dir, year)
      - plots_carbonPrices.plot_minMax(prices_usd_max, output_path)
    """
    # Year for which you want the plot
    year = 2024

    # Location of the underlying WCPD USD price files (relative to repo root)
    carbon_price_dir = (
        REPO_ROOT
        / "_raw"
        / "wcpd_usd"
        / "CO2"
        / "constantPrices"
        / "FixedXRate"
    )

    # Call the existing function with the required arguments
    df, prices_usd_max = prepare_carbon_price_data(
        data_dir=str(carbon_price_dir),
        year=year,
    )

    # Save underlying data to the unified dataFig directory
    data_path = DATA_DIR / f"carbonPrices_usd_max_{year}.csv"
    prices_usd_max.to_csv(data_path, index=False)

    # Produce the plot into the unified plots directory
    plot_path = PLOTS_DIR / f"max_price_ecp_{year}.png"
    plot_minMax(prices_usd_max, output_path=plot_path)

    return ChartRun(
        id=f"carbon_price_minmax_{year}",
        title=f"Emissions-weighted carbon prices – min/max range ({year})",
        module="proc_carbonPrices/plots_carbonPrices",
        function="prepare_carbon_price_data → plot_minMax",
        plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
        data_file=str(data_path.relative_to(OUTPUT_ROOT)),
        params={"year": year, "data_dir": str(carbon_price_dir)},
    )



def run_coverage_latest() -> ChartRun:
    """
    Coverage bar chart for European countries vs world average, latest year.
    Relies on:
      - plots_coverage.coverage_plots(coverage, year, output_plot_path, output_data_path)
    """
    coverage_path = REPO_ROOT / "_output" / "_dataset" / "coverage" / "tot_coverage_jurisdiction_CO2.csv"
    coverage = pd.read_csv(coverage_path)

    year = int(coverage["year"].max())

    plot_path = PLOTS_DIR / f"coverage_{year}.png"
    data_path = DATA_DIR / f"coverage_{year}.csv"

    coverage_plots(
        coverage=coverage,
        year=year,
        output_plot_path=plot_path,
        output_data_path=data_path,
    )

    return ChartRun(
        id=f"coverage_{year}",
        title=f"Share of CO₂ emissions covered by carbon pricing – {year}",
        module="plots_coverage",
        function="coverage_plots",
        plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
        data_file=str(data_path.relative_to(OUTPUT_ROOT)),
        params={"year": year},
    )


def run_world_sectors_2024() -> ChartRun:
    """
    World average carbon prices by sector for 2024 (bar chart).
    Relies on:
      - plots_world_sectors.plot_world_sectors(data_dir)
    """
    plot_path = PLOTS_DIR / "world_sector_prices_2024.png"
    data_path = DATA_DIR / "world_sector_prices_2024.csv"

    data_dir = REPO_ROOT / "_output" / "_dataset"

    # In your refactored version, have plot_world_sectors accept explicit output paths:
    # plot_world_sectors(
    #     data_dir=data_dir,
    #     output_plot_path=plot_path,
    #     output_data_path=data_path,
    # )
    # For now we just call it, assuming it writes to the right place internally.
    plot_world_sectors(data_dir=data_dir)

    return ChartRun(
        id="world_sectors_2024",
        title="World carbon prices by sector – 2024",
        module="plots_world_sectors",
        function="plot_world_sectors",
        plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
        data_file=str(data_path.relative_to(OUTPUT_ROOT)),
        params={"year": 2024},
    )


def run_ets_tax_selected_jurisdictions_2024() -> ChartRun:
    """
    ETS + carbon tax prices for selected jurisdictions (2024).
    Relies on:
      - plots_ets_tax_jur.plot_selected_jurisdictions(data_dir, jurisdictions, output_plot_path, output_data_path)
    """
    data_dir = REPO_ROOT / "_output" / "_dataset"

    selected_jurisdictions = [
        "World",
        "European Union (ETS)",
        "Germany",
        "France",
        "United Kingdom",
        "Canada",
        "United States",
        "China",
        "Japan",
        "Korea, Republic of",
    ]

    plot_path = PLOTS_DIR / "ets_tax_selected_jurisdictions_2024.png"
    data_path = DATA_DIR / "ets_tax_selected_jurisdictions_2024.csv"

    plot_selected_jurisdictions(
        data_dir=data_dir,
        jurisdictions=selected_jurisdictions,
        output_plot_path=plot_path,
        output_data_path=data_path,
    )

    return ChartRun(
        id="ets_tax_selected_jurisdictions_2024",
        title="ETS and carbon tax prices by jurisdiction – 2024",
        module="plots_ets_tax_jur",
        function="plot_selected_jurisdictions",
        plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
        data_file=str(data_path.relative_to(OUTPUT_ROOT)),
        params={"year": 2024, "jurisdictions": selected_jurisdictions},
    )


def run_subnational_stacks() -> List[ChartRun]:
    """
    Subnational stacked coverage charts for US, Canada, China,
    plus a national stack chart.
    """
    ecp_path = REPO_ROOT / "_output" / "_dataset" / "ecp" / "ipcc" / "ecp_economy" / "ecp_CO2.csv"
    df = pd.read_csv(ecp_path)

    runs: List[ChartRun] = []

    for label, subset, file_stub in [
        ("United States", df[df["jurisdiction"].isin(US_STATES)], "us_subnational_stack"),
        ("Canada", df[df["jurisdiction"].isin(CANADIAN_PROVINCES)], "canada_subnational_stack"),
        ("China", df[df["jurisdiction"].isin(CHINA_PROVINCES)], "china_subnational_stack"),
    ]:
        plot_path = PLOTS_DIR / f"{file_stub}.png"
        data_path = DATA_DIR / f"{file_stub}.csv"

        plot_filtered_stacked_bar(
            df_country=subset,
            country_name=label,
            output_plot_path=plot_path,
            output_data_path=data_path,
        )

        runs.append(
            ChartRun(
                id=file_stub,
                title=f"Carbon price coverage – {label} subnational jurisdictions",
                module="plots_subnat_stacked",
                function="plot_filtered_stacked_bar",
                plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
                data_file=str(data_path.relative_to(OUTPUT_ROOT)),
                params={"region": label},
            )
        )

    # National stack
    national_input_path = Path("/Users/geoffroydolphin/GitHub/ECP/_output/_figures/dataFig") / "national_stacked_world.csv"
    df_national = pd.read_csv(national_input_path)

    plot_path = PLOTS_DIR / "national_stack.png"
    data_path = DATA_DIR / "national_stack.csv"

    plot_stacked_national_bar(
        df=df_national,
        output_plot_path=plot_path,
        output_data_path=data_path,
    )

    runs.append(
        ChartRun(
            id="national_stack",
            title="Carbon price coverage – national jurisdictions",
            module="plots_national_stacked",
            function="plot_stacked_national_bar",
            plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
            data_file=str(data_path.relative_to(OUTPUT_ROOT)),
            params={},
        )
    )

    return runs


# --------------------------------------------------------------------------------------
# NEW chart runners (cp_gdp, cp_ts, cp_regional, ccost_gdp, coverage_heatmaps)
# --------------------------------------------------------------------------------------

def run_cp_gdp_latest() -> ChartRun:
    """
    GDP coverage by carbon pricing (latest year).
    Relies on:
      - plots_cp_gdp.plot_cp_gdp(df, year, ...)
    """
    gdp_path = REPO_ROOT / "_output" / "_dataset" / "coverage" / "cpriceCoverageGDP.csv"
    df_gdp = pd.read_csv(gdp_path)

    year = int(df_gdp["year"].max())

    plot_path = PLOTS_DIR / f"cp_gdp_{year}.png"
    data_path = DATA_DIR / f"cp_gdp_{year}.csv"

    plot_cp_gdp(
        df=df_gdp,
        year=year,
        coverage_col="cpCoverage",
        jurisdiction_col="jurisdiction",
        year_col="year",
        output_plot_path=plot_path,
        output_data_path=data_path,
        title=f"GDP coverage by carbon pricing – {year}",
    )

    return ChartRun(
        id=f"cp_gdp_{year}",
        title=f"GDP coverage by carbon pricing – {year}",
        module="plots_cp_gdp",
        function="plot_cp_gdp",
        plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
        data_file=str(data_path.relative_to(OUTPUT_ROOT)),
        params={"year": year},
    )


def run_cp_ts_selected_jurisdictions(top_n: int = 8) -> ChartRun:
    """
    Time series of carbon prices for top-N jurisdictions by latest-year price.
    Relies on:
      - plots_cp_ts.plot_cp_ts_jurisdictions(...)
    """
    ecp_path = REPO_ROOT / "_output" / "_dataset" / "ecp" / "ipcc" / "ecp_economy" / "ecp_CO2.csv"
    df = pd.read_csv(ecp_path)

    latest_year = int(df["year"].max())

    df_latest = df[df["year"] == latest_year].copy()
    df_latest = df_latest.dropna(subset=["ecp_all_jurCO2_usd_k"])
    df_latest = df_latest.sort_values("ecp_all_jurCO2_usd_k", ascending=False)

    top_jurisdictions = df_latest["jurisdiction"].head(top_n).tolist()

    plot_path = PLOTS_DIR / "cp_ts_jurisdictions.png"
    data_path = DATA_DIR / "cp_ts_jurisdictions.csv"

    plot_cp_ts_jurisdictions(
        df=df,
        jurisdictions=top_jurisdictions,
        year_col="year",
        jurisdiction_col="jurisdiction",
        value_col="ecp_all_jurCO2_usd_k",
        output_plot_path=plot_path,
        output_data_path=data_path,
        title="Emissions-weighted CO₂ price – selected jurisdictions",
    )

    return ChartRun(
        id="cp_ts_jurisdictions",
        title="Emissions-weighted CO₂ price – selected jurisdictions",
        module="plots_cp_ts",
        function="plot_cp_ts_jurisdictions",
        plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
        data_file=str(data_path.relative_to(OUTPUT_ROOT)),
        params={"top_n": top_n, "jurisdictions": top_jurisdictions},
    )


def run_cp_ts_world_sectors() -> ChartRun:
    """
    Time series of world average carbon prices by sector.
    Relies on:
      - plots_cp_ts.plot_cp_ts_world_sectors(...)
    """
    world_sec_path = (
        REPO_ROOT
        / "_output"
        / "_dataset"
        / "ecp"
        / "ipcc"
        / "ecp_world_sectors"
        / "world_sectoral_ecp_CO2.csv"
    )
    df_world_sec = pd.read_csv(world_sec_path)

    plot_path = PLOTS_DIR / "cp_ts_world_sectors.png"
    data_path = DATA_DIR / "cp_ts_world_sectors.csv"

    plot_cp_ts_world_sectors(
        df_world_sec=df_world_sec,
        sector_map=WORLD_SECTOR_MAP,
        year_col="year",
        sector_col="ipcc_code",
        value_col="ecp_all_sectCO2_usd_k",
        output_plot_path=plot_path,
        output_data_path=data_path,
        title="Emissions-weighted CO₂ price – world sectors",
    )

    return ChartRun(
        id="cp_ts_world_sectors",
        title="Emissions-weighted CO₂ price – world sectors",
        module="plots_cp_ts",
        function="plot_cp_ts_world_sectors",
        plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
        data_file=str(data_path.relative_to(OUTPUT_ROOT)),
        params={},
    )


def run_cp_regional() -> ChartRun:
    """
    Regional average carbon price time series.
    Relies on:
      - plots_cp_regional.plot_cp_regional(...)
    """
    regional_path = REPO_ROOT / "_output" / "_dataset" / "ecp" / "ipcc" / "ecp_economy" / "ecp_CO2_regional.csv"
    df_reg = pd.read_csv(regional_path)

    plot_path = PLOTS_DIR / "cp_ts_regional.png"
    data_path = DATA_DIR / "cp_ts_regional.csv"

    # NOTE: adjust `value_col` if the column name in ecp_CO2_regional.csv differs.
    plot_cp_regional(
        df=df_reg,
        region_col="region",
        year_col="year",
        value_col="CO2_price", 
        regions=None,
        output_plot_path=plot_path,
        output_data_path=data_path,
        title="Emissions-weighted CO₂ price – regional averages",
    )

    return ChartRun(
        id="cp_ts_regional",
        title="Emissions-weighted CO₂ price – regional averages",
        module="plots_cp_regional",
        function="plot_cp_regional",
        plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
        data_file=str(data_path.relative_to(OUTPUT_ROOT)),
        params={},
    )


def run_ccost_gdp_latest() -> ChartRun:
    """
    Carbon cost and CO₂ emissions per unit of GDP (latest year).
    Relies on:
      - plots_ccost_gdp.plot_ccost_gdp(...)
    """
    ccost_path = REPO_ROOT / "_output" / "_dataset" / "carbonCost" / "carbonCostTot.csv"
    df_cost = pd.read_csv(ccost_path)

    if "year" in df_cost.columns:
        year = int(df_cost["year"].max())
        df_latest = df_cost[df_cost["year"] == year].copy()
    else:
        year = None
        df_latest = df_cost.copy()

    plot_path = PLOTS_DIR / "carbon_cost.png"
    data_path = DATA_DIR / "carbon_cost.csv"

    title = "Carbon cost and CO₂ emissions per unit of GDP"
    if year is not None:
        title = f"{title} ({year})"

    plot_ccost_gdp(
        df=df_latest,
        jurisdiction_col="regionName",
        ccost_col="ccost_int",
        emissions_col="co2_int",
        output_plot_path=plot_path,
        output_data_path=data_path,
        title=title,
        x_label="Carbon cost (% of GDP)",
    )

    return ChartRun(
        id="carbon_cost_gdp",
        title=title,
        module="plots_ccost_gdp",
        function="plot_ccost_gdp",
        plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
        data_file=str(data_path.relative_to(OUTPUT_ROOT)),
        params={"year": year} if year is not None else {},
    )


def run_coverage_heatmaps() -> List[ChartRun]:
    """
    Coverage heatmaps for:
      - national jurisdictions with any positive coverage
      - subnational jurisdictions (US, Canada, China)
      - world sectors
    """
    runs: List[ChartRun] = []

    cov_jur_path = REPO_ROOT / "_output" / "_dataset" / "coverage" / "tot_coverage_jurisdiction_CO2.csv"
    cov_world_sec_path = REPO_ROOT / "_output" / "_dataset" / "coverage" / "tot_coverage_world_sectors_CO2.csv"

    cov_jur = pd.read_csv(cov_jur_path)
    cov_world_sec = pd.read_csv(cov_world_sec_path)

    cov_jur["year"] = pd.to_numeric(cov_jur["year"], errors="coerce")
    cov_world_sec["year"] = pd.to_numeric(cov_world_sec["year"], errors="coerce")

    # Jurisdictions with any positive coverage
    positive_jurs = (
        cov_jur.loc[cov_jur["cov_all_CO2_jurCO2"] > 0, "jurisdiction"]
        .dropna()
        .unique()
        .tolist()
    )

    # Separate national vs subnational (approximate separation using province/state lists)
    subnat_jurs = set(CANADIAN_PROVINCES + US_STATES + CHINA_PROVINCES)
    national_jurs = [j for j in positive_jurs if j not in subnat_jurs]

    # --- National jurisdictions heatmap ---
    data_nat = cov_jur[cov_jur["jurisdiction"].isin(national_jurs)].copy()

    plot_path = PLOTS_DIR / "coverage_hm_national.png"
    data_path = DATA_DIR / "coverage_hm_national.csv"

    plot_coverage_heatmap(
        df=data_nat,
        index_col="jurisdiction",
        column_col="year",
        value_col="cov_all_CO2_jurCO2",
        title="CO₂ coverage: national jurisdictions (1990–latest)",
        output_plot_path=plot_path,
        output_data_path=data_path,
    )

    runs.append(
        ChartRun(
            id="coverage_hm_national",
            title="CO₂ coverage: national jurisdictions (1990–latest)",
            module="plots_coverage_heatmaps",
            function="plot_coverage_heatmap",
            plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
            data_file=str(data_path.relative_to(OUTPUT_ROOT)),
            params={"type": "national"},
        )
    )

    # --- Subnational heatmaps: US, Canada, China ---
    for label, subset_jurs, stub in [
        ("United States subnational", US_STATES, "us_subnational"),
        ("Canada subnational", CANADIAN_PROVINCES, "canada_subnational"),
        ("China subnational", CHINA_PROVINCES, "china_subnational"),
    ]:
        data_sub = cov_jur[cov_jur["jurisdiction"].isin(subset_jurs)].copy()
        if data_sub.empty:
            continue

        plot_path = PLOTS_DIR / f"coverage_hm_{stub}.png"
        data_path = DATA_DIR / f"coverage_hm_{stub}.csv"

        plot_coverage_heatmap(
            df=data_sub,
            index_col="jurisdiction",
            column_col="year",
            value_col="cov_all_CO2_jurCO2",
            title=f"CO₂ coverage: {label} (1990–latest)",
            output_plot_path=plot_path,
            output_data_path=data_path,
        )

        runs.append(
            ChartRun(
                id=f"coverage_hm_{stub}",
                title=f"CO₂ coverage: {label} (1990–latest)",
                module="plots_coverage_heatmaps",
                function="plot_coverage_heatmap",
                plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
                data_file=str(data_path.relative_to(OUTPUT_ROOT)),
                params={"type": "subnational", "region": label},
            )
        )

    # --- World sectors heatmap ---
    data_world_sec = cov_world_sec[
        cov_world_sec["ipcc_code"].isin(WORLD_SECTOR_MAP.keys())
    ].copy()

    plot_path = PLOTS_DIR / "coverage_hm_world_sectors.png"
    data_path = DATA_DIR / "coverage_hm_world_sectors.csv"

    plot_coverage_heatmap(
        df=data_world_sec,
        index_col="ipcc_code",
        column_col="year",
        value_col="cov_all_CO2_WldSectCO2",
        title="CO₂ coverage: world sectors (1990–latest)",
        output_plot_path=plot_path,
        output_data_path=data_path,
    )

    runs.append(
        ChartRun(
            id="coverage_hm_world_sectors",
            title="CO₂ coverage: world sectors (1990–latest)",
            module="plots_coverage_heatmaps",
            function="plot_coverage_heatmap",
            plot_file=str(plot_path.relative_to(OUTPUT_ROOT)),
            data_file=str(data_path.relative_to(OUTPUT_ROOT)),
            params={"type": "world_sectors"},
        )
    )

    return runs


# --------------------------------------------------------------------------------------
# Master list of chart runners
# --------------------------------------------------------------------------------------

def run_all_charts() -> List[ChartRun]:
    registry: List[ChartRun] = []

    # Original charts
    registry.append(run_carbon_price_minmax())
    registry.append(run_coverage_latest())
    registry.append(run_world_sectors_2024())
    registry.append(run_ets_tax_selected_jurisdictions_2024())
    registry.extend(run_subnational_stacks())

    # New charts
    #registry.append(run_cp_gdp_latest())
    registry.append(run_cp_ts_selected_jurisdictions())
    registry.append(run_cp_ts_world_sectors())
    registry.append(run_cp_regional())
    registry.append(run_ccost_gdp_latest())
    registry.extend(run_coverage_heatmaps())

    return registry


# --------------------------------------------------------------------------------------
# CLI entry point
# --------------------------------------------------------------------------------------

def main() -> None:
    print(f"Using OUTPUT_ROOT={OUTPUT_ROOT}")
    runs = run_all_charts()

    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRY_PATH.open("w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in runs], f, indent=2)

    print(f"✅ Generated {len(runs)} charts.")
    print(f"📒 Registry written to: {REGISTRY_PATH}")


if __name__ == "__main__":
    main()
