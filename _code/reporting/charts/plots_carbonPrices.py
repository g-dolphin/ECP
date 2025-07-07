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

# CHART-SPECIFIC PLOT FEATURES

def plot_minMax(prices_usd_max, path):
    prices_usd_max = pd.read_csv(path+r"/carbonPrices_usd_max_2024.csv")
    #coverage = pd.read_csv(path_input+r"/carbonPrices_coverage.csv")

    #colors = plt.cm.viridis(np.linspace(0, 0.5, len(prices_usd_max)))
    color_bars = ["lightsteelblue"]

    # PLOTS
    wld_avg = prices_usd_max.loc[(prices_usd_max.jurisdiction=="World") & (prices_usd_max.year==2024)]["ecp_all_jurCO2_usd_k"].item()

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
    plt.savefig(r"/Users/gd/GitHub/ECP/_output/_figures/plots/max_price_ecp_2024.png")
    plt.close()

    return
