#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:40:15 2021

@author: GD
"""

# Script for plots 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (8,6)
plt.rcParams['font.size'] = 12

pd.set_option('display.max_columns', None)

user_root_path = "/Users/gd/GitHub"
git_repo_path = "/ECP"

output_dir = ""

# COVERAGE

df_cov = pd.read_csv(user_root_path+git_repo_path+"/coverage/total_coverage.csv")

df_cov = df_cov.loc[df_cov['Year']>=1990]
df_cov = df_cov.loc[df_cov['Year']<=2018]

# only keep countries for which coverage becomes >0 at least once in the sample
jur_list = df_cov.loc[df_cov['cov_tax_ets_share_jurGHG']>0, "Jurisdiction"].unique() 
df_cov = df_cov.loc[df_cov.Jurisdiction.isin(jur_list), :]


## Heatmap

df_cov_hm = df_cov.pivot(index='Jurisdiction', columns='Year', values='cov_tax_ets_share_jurGHG')

plt.subplots(figsize=(20,15))
#ax=subplot(111)

cmap = sns.cm.rocket_r
#sns.set(font_scale=1)
sns.heatmap(df_cov_hm, vmin=0, vmax=1,cmap=cmap,annot_kws={"size": 36})

plt.savefig(output_dir+"/cov_hm.pdf")
plt.close()


# PRICES

df_prices_econ = pd.read_csv(user_root_path+git_repo_path+"/price/ecp_economy/ecp_vw/ecp.csv")
df_prices_sect = pd.read_csv(user_root_path+git_repo_path+"/price/ecp_sectors/ecp_vw/ecp_sector.csv")

cntries_list = ['Argentina', 'Austria', 'Belgium', 'Bulgaria', 'Chile', 'Colombia',
       'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia',
       'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
       'Ireland', 'Italy', 'Japan', 'Latvia', 'Lithuania', 'Luxembourg',
       'Malta', 'Mexico', 'Netherlands', 'Norway', 'Poland', 'Portugal',
       'Romania', 'Slovak Republic', 'Slovenia', 'Spain', 'Sweden',
       'Switzerland', 'Ukraine', 'United Kingdom']

## Jurisdiction

fig = plt.figure(figsize=(18,12))

for ctry in cntries_list:
    temp_econ = df_prices_econ.loc[df_prices_econ.Jurisdiction==ctry, :]
    plt.plot(temp_econ.Year, temp_econ.ECP_tax_ets_jurGHG_2019USD, label=ctry)

plt.title("Emission coverage by carbon pricing schemes, by jurisdiction", fontsize=26)
plt.ylabel("% of jurisdiction's total GHG emissions", fontsize=24)

plt.xlim([1990, 2018])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, 
           shadow=False, ncol=6)

plt.tight_layout()
plt.show()
plt.close()

## Sectors
sectors = ["ABFLOW003", "ABFLOW012", "ABFLOW028"]


selec_conditions = (df_prices_sect.Jurisdiction.isin(cntries_list)) & (df_prices_sect.Flow.isin(sectors)) & (df_prices_sect.Year==2018) 
temp_sect = df_prices_sect.loc[selec_conditions, ["Jurisdiction", "Year", "Flow", "Total_ew_price_sector_2019USD"]]


fig = plt.figure(figsize=(18,12))

# set width of bars
barWidth = 0.25

# set heights of bars
bars1 = np.array(temp_sect.loc[temp_sect.Flow=="ABFLOW003", "Total_ew_price_sector_2019USD"])
bars2 = np.array(temp_sect.loc[temp_sect.Flow=="ABFLOW012", "Total_ew_price_sector_2019USD"])
bars3 = np.array(temp_sect.loc[temp_sect.Flow=="ABFLOW028", "Total_ew_price_sector_2019USD"])
 
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
plt.xticks([r + barWidth for r in range(len(bars1))], cntries_list, rotation=90)
 
# Create legend & Show graphic
plt.legend()
plt.show()





