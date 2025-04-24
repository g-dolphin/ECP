#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 11:47:01 2021

@author: gd
"""

import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import ListedColormap
from turtle import color
import os
import pandas as pd
import numpy as np
from pathlib import Path


## PATHS

prices_economy = pd.read_csv(r"/Users/gd/Library/CloudStorage/OneDrive-rff/Documents/Research/projects/ecp/ecp_dataset/data/ecp/ecp_economy/ecp_vw/ecp_tv_CO2_Apr-24-2025.csv")
prices_usd_max = pd.read_csv(r"/Users/gd/GitHub/ECP/_figures/dataFig/carbonPrices_usd_max_2024.csv")
#coverage = pd.read_csv(path_input+r"/carbonPrices_coverage.csv")

# CHART-SPECIFIC PLOT FEATURES

#colors = plt.cm.viridis(np.linspace(0, 0.5, len(prices_usd_max)))
color_bars = ["lightsteelblue"]

# PLOTS
wld_avg = prices_economy.loc[(prices_economy.jurisdiction=="World") & (prices_economy.year==2024)]["ecp_all_jurCO2_usd_k"].item()

# Sort the data by ecp_all_jurCO2_usd_k
sorted_data = prices_usd_max.sort_values(by="ecp_all_jurCO2_usd_k", ascending=True)
sorted_data = sorted_data[sorted_data.ecp_all_jurCO2_usd_k!=0]
sorted_data = sorted_data[sorted_data.jurisdiction!='Malta']

# Extract sorted values
labels = sorted_data['jurisdiction']  # Or whatever column you're using for labels
y_pos = range(len(labels))  # New positions
prices = sorted_data['ecp_all_jurCO2_usd_k']
max_prices = sorted_data['max_price']

plt.figure(figsize=(10, 16))  # Adjusted for vertical layout

# Plot horizontal bars
ax1 = plt.barh(y_pos, prices, color=color_bars, label="Average (emissions-weighted)")
ax2 = plt.barh(y_pos, max_prices, height=0.6, facecolor=(1,1,1,0), edgecolor=".2", linewidth=1.5, label="Maximum price")

# World average line
plt.axvline(x=wld_avg, color="firebrick", linestyle='--', label="World average")

plt.xticks(size=18, color="gray")
plt.yticks(ticks=y_pos, labels=labels, size=18, color="gray")
plt.xlabel("2021USD/tCO$_2$", size=18, color="gray")
plt.legend(loc="lower right", fontsize=16)

plt.tight_layout()
plt.savefig(r"/Users/gd/GitHub/ECP/_figures/plots/max_price_ecp_2024.png")
plt.close()

#------------------------------------ Time series:ecp, economy-wide, CO2 ------------------------------------#

countries_eur = ["Austria", "Belgium", "Croatia", "France", "Germany", "Italy", "Romania",
                 "Slovenia", "Spain", "United Kingdom", "Ukraine"]

prices_economy = prices_economy.loc[prices_economy.jurisdiction.isin(countries_eur), :]

fig, ax = plt.subplots(figsize=(14,10))

matplotlib.rc('axes', edgecolor='gray')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(True)

plt.title("Average CO$_2$ price, 1990-2022", color="gray", fontsize=24)

i = 0

for jur in countries_eur:
    temp = prices_economy.loc[prices_economy.jurisdiction==jur, :]
    ax.plot(temp.year, temp.ecp_all_jurCO2_usd_k, label=jur, linewidth=2.5, color=colors[i])
    i += 1

ax.set(facecolor = "white")
ax.set_xlim(1990, 2022)
ax.set_ylim(0, 100)
ax.grid(axis='y')

ax.set_ylabel("2021USD/tCO$_2$", fontsize=18)
ax.tick_params(labelsize=20)

ax.legend(bbox_to_anchor=(0.5,-0.2), facecolor = "white",
            loc="lower center", fontsize=16, ncol=6)   

plt.tight_layout()
plt.savefig(path_output+r"\ecp_co2_ts_eur.png",
            bbox_inches="tight", edgecolor="gray")

plt.close()

#------------------------------------ Bar chart: coverage ------------------------------------#

wldAvgCov = coverage.loc[(coverage.jurisdiction=="World") & (coverage.year==2022)]["cov_all_CO2_jurCO2"].item()
coverage = coverage.loc[coverage.jurisdiction.isin(countries_eur), :]

y_pos = np.arange(len(coverage.jurisdiction.unique()))
labels = list(coverage.jurisdiction.unique())

plt.figure(figsize=(10, 16))

ax1 = plt.barh(y_pos, coverage.cov_all_CO2_jurCO2*100,
               color=color_bars) #

ax2 = plt.axvline(x=wldAvgCov*100, color="firebrick", linestyle='--', label="World average")

#plt.title("CO$_2$ prices in Europe (2021)",
#          size=22)
plt.xticks(size=18, color="gray")
plt.yticks(ticks=y_pos, labels=labels, size=18, color="gray") #na_jur

plt.xlabel("Percent of total CO$_2$ emissions", size=18, color="gray")
plt.legend(loc="upper right", fontsize=16)

plt.tight_layout()

plt.savefig(path_output+r"\coverage2022.png")
plt.close()



