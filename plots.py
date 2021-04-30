#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:40:15 2021

@author: GD
"""

# Basic plots #

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (8,6)
plt.rcParams['font.size'] = 12

pd.set_option('display.max_columns', None)

price_sector = pd.read_csv("/Users/GD/Documents/GitHub/ECP/price/ecp_sectors/ecp_vw/ecp_sector.csv")

sectors = ["ABFLOW003", "ABFLOW012", "ABFLOW028"]
countries = ['Argentina', 'Austria', 'Belgium', 'Bulgaria', 'Chile', 'Colombia',
       'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia',
       'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
       'Ireland', 'Italy', 'Japan', 'Latvia', 'Lithuania', 'Luxembourg',
       'Malta', 'Mexico', 'Netherlands', 'Norway', 'Poland', 'Portugal',
       'Romania', 'Slovak Republic', 'Slovenia', 'Spain', 'Sweden',
       'Switzerland', 'Ukraine', 'United Kingdom']

selec_conditions = (price_sector.Jurisdiction.isin(countries)) & (price_sector.Flow.isin(sectors)) & (price_sector.Year==2018) 

price_sector = price_sector.loc[selec_conditions, ["Jurisdiction", "Year", "Flow", "Total_ew_price_sector_2019USD"]]


fig = plt.figure(figsize=(18,12))

# set width of bars
barWidth = 0.25

# set heights of bars
bars1 = np.array(price_sector.loc[price_sector.Flow=="ABFLOW003", "Total_ew_price_sector_2019USD"])
bars2 = np.array(price_sector.loc[price_sector.Flow=="ABFLOW012", "Total_ew_price_sector_2019USD"])
bars3 = np.array(price_sector.loc[price_sector.Flow=="ABFLOW028", "Total_ew_price_sector_2019USD"])
 
# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
 
# Make the plot
plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Power')
plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='Industry')
plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='Transport')
 
# Add xticks on the middle of the group bars
plt.xlabel('group', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(bars1))], countries, rotation=90)
 
# Create legend & Show graphic
plt.legend()
plt.show()