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
from matplotlib.lines import Line2D

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (8,6)
plt.rcParams['font.size'] = 12
plt.rcParams.update({'axes.facecolor':'lavender'})

pd.set_option('display.max_columns', None)

user_root_path = "/Users/gd/GitHub"
git_repo_path = "/ECP"

#output_dir = ""
output_dir = "/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/working_paper/figures"


ipcc_sector = ["1A1A1", "1A1B", "1A2A", "1A2C", "1A2D", "1A2I", 
               "1A3B", "1A4A", "1A4B"]

ipcc_sector_labels = {"1A1A1":"Power generation", "1A1B":"Petroleum refining", 
                      "1A2A":"Iron and Steel", "1A2C":"Chemicals", 
                      "1A2D":"Pulp, Paper and Print", "1A2I":"Mining and Quarrying", 
                      "1A3B":"Road transport", "1A4A":"Buildings (commercial/institutional)",
                      "1A4B":"Buildings (residential)"}

iea_sectors = ["ABFLOW003", "ABFLOW012", "ABFLOW028"]

cntries_list = ['Argentina', 'Austria', 'Belgium', 'Bulgaria', 'Chile', 'Colombia',
       'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia',
       'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
       'Ireland', 'Italy', 'Japan', 'Latvia', 'Lithuania', 'Luxembourg',
       'Malta', 'Mexico', 'Netherlands', 'Norway', 'Poland', 'Portugal',
       'Romania', 'Slovak Republic', 'Slovenia', 'Spain', 'Sweden',
       'Switzerland', 'Ukraine', 'United Kingdom']

df_cov = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/data/coverage/total_coverageII.csv")
#df_cov = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/data/coverage/world_sectoral_coverage.csv")

df_prices_econ = pd.read_csv(user_root_path+git_repo_path+"/price/ecp_economy/ecp_vw/ecp_tvII.csv")
df_prices_sect = pd.read_csv(user_root_path+git_repo_path+"/price/ecp_sectors/ecp_vw/ecp_sector.csv")
df_prices_sect_wld = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/data/ecp/ecp_sectors_wld/world_sectoral_ecp.csv")




# COVERAGE


df_cov = df_cov.loc[df_cov['Year']>=1990]
df_cov = df_cov.loc[df_cov['Year']<=2020]

# only keep countries for which coverage becomes >0 at least once in the sample
jur_list = df_cov.loc[df_cov['cov_all_CO2_jurCO2']>0, "Jurisdiction"].unique() 

df_cov = df_cov.loc[df_cov.Jurisdiction.isin(list(jur_list)+["World"]), :]
df_cov["cov_all_CO2_jurCO2"] = df_cov["cov_all_CO2_jurCO2"]*100

## Heatmap of jurisdiction-level coverage

df_cov_hm = df_cov.pivot(index='Jurisdiction', columns='Year', values='cov_all_CO2_jurCO2')

plt.subplots(figsize=(20,15))
#ax=subplot(111)

cmap = sns.cm.rocket_r
#sns.set(font_scale=1)
ax = sns.heatmap(df_cov_hm, vmin=0, vmax=100,cmap=cmap,annot_kws={"size": 46},
                 cbar_kws={'label': '%'})

ax.figure.axes[-1].yaxis.label.set_size(20)

plt.title("Share of jurisdiction CO$_2$ emissions covered by carbon pricing mechanisms, by jurisdiction",
          fontsize=26)

plt.xlabel("")
plt.xticks(rotation=45, size=17)
plt.ylabel("Jurisdiction", fontsize=22)

plt.tight_layout()
plt.savefig(output_dir+"/cov_hm.pdf")
plt.close()

## Heatmap of world sector-level coverage

df_cov = df_cov.loc[df_cov.IPCC_cat_code.isin(ipcc_sector), :]
df_cov["cov_all_CO2_WldSectCO2"] = df_cov["cov_all_CO2_WldSectCO2"]*100

df_cov_hm = df_cov.pivot(index='IPCC_cat_code', columns='Year', values='cov_all_CO2_WldSectCO2')

plt.subplots(figsize=(20,15))
#ax=subplot(111)

cmap = sns.cm.crest
#sns.set(font_scale=1)
ax = sns.heatmap(df_cov_hm, vmin=0, vmax=50,cmap=cmap,annot_kws={"size": 46},
                 cbar_kws={'label': '%'})

ax.figure.axes[-1].yaxis.label.set_size(20)

ax.set_yticklabels(["Power generation", "Petroleum refining", "Iron and Steel", 
                    "Chemicals", "Pulp, Paper and Print", "Mining and Quarrying", 
                    "Road transport", "Commercial/Institutional", "Residential"],
                    rotation=0, size=18)

plt.title("Share of world CO$_2$ emissions covered by carbon pricing mechanism, by sector",
          fontsize=26)
plt.ylabel("IPCC source categories", fontsize=22)
plt.xlabel("")
plt.xticks(rotation=45, size=17)
plt.tight_layout()

plt.savefig(output_dir+"/cov_sect_hm.pdf")
plt.close()

# PRICES

df_prices_econ = df_prices_econ.loc[df_prices_econ['Year']>=1990]
df_prices_econ = df_prices_econ.loc[df_prices_econ['Year']<=2018]

df_prices_sect = df_prices_sect.loc[df_prices_sect['Year']>=1990]
df_prices_sect = df_prices_sect.loc[df_prices_sect['Year']<=2018]


## Jurisdiction

fig = plt.figure(figsize=(18,12))

for ctry in cntries_list:
    temp_econ = df_prices_econ.loc[df_prices_econ.Jurisdiction==ctry, :]
    plt.plot(temp_econ.Year, temp_econ.ecp_all_jurGHG_2019USD, label=ctry)

plt.title("Emissions price, by jurisdiction", fontsize=26)
plt.ylabel("2019 USD / tCO2", fontsize=24)

plt.xlim([1990, 2018])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, 
           shadow=False, ncol=6)

plt.tight_layout()

plt.savefig("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/working_paper/figures/coverage.pdf")

plt.close()

## Sectors
sectors = ["ABFLOW003", "ABFLOW012", "ABFLOW028"]


# Multi-sector bar plot 2018

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

# Multi-sector heatmap

sector003 = df_prices_sect.loc[(df_prices_sect.Jurisdiction.isin(cntries_list)) & (df_prices_sect.Flow=="ABFLOW003")]
sector012 = df_prices_sect.loc[(df_prices_sect.Jurisdiction.isin(cntries_list)) & (df_prices_sect.Flow=="ABFLOW012")]
sector028 = df_prices_sect.loc[(df_prices_sect.Jurisdiction.isin(cntries_list)) & (df_prices_sect.Flow=="ABFLOW028")]

vmin = min(sector003.Total_ew_price_sector_2019USD.min(), sector012.Total_ew_price_sector_2019USD.min())
vmax = max(sector003.Total_ew_price_sector_2019USD.max(), sector012.Total_ew_price_sector_2019USD.max())

fig, axs = plt.subplots(ncols=3, gridspec_kw=dict(width_ratios=[4,1,0.2]))

sector003_hm = sector003.pivot(index='Jurisdiction', columns='Year', values='Total_ew_price_sector_2019USD')
sector012_hm = sector012.pivot(index='Jurisdiction', columns='Year', values='Total_ew_price_sector_2019USD')

sns.heatmap(sector003_hm, annot=True, cbar=False, ax=axs[0], vmin=vmin)
sns.heatmap(sector012_hm, annot=True, yticklabels=False, cbar=False, ax=axs[1], vmax=vmax)

fig.colorbar(axs[1].collections[0], cax=axs[2])

plt.subplots(figsize=(20,15))
sns.heatmap(sector003_hm, vmin=sector003.Total_ew_price_sector_2019USD.min(), 
            vmax=sector003.Total_ew_price_sector_2019USD.max(),cmap=cmap,annot_kws={"size": 36})

# Sector-level density plots, 2020

fig, axs = plt.subplots(ncols=3, sharey=True)

i = 0

for sector in iea_sectors:
    temp_df = df_prices_sect.loc[(df_prices_sect.Flow==sector) & (df_prices_sect.Year==2018), :]
    density = sns.histplot(data=temp_df.Total_ew_price_sector_2019USD, bins=50,
                           stat="probability", legend=True, kde=True, ax=axs[i])
    density.set(ylim=[0,0.2], title=sectors[i], xlabel="")
    i+=1

fig.suptitle("Carbon price density, by sector")
plt.xlabel("CO$_2$ price (/tCO$_2$e)")

fig.savefig("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/working_paper/figures/cp_density_sector_2018.pdf")


sns.boxplot(x="Flow", y="Total_ew_price_sector_2019USD", 
            data=df_prices_sect.loc[(df_prices_sect.Flow.isin(sectors)) & (df_prices_sect.Year==2018), :])


## Sectors world

markers = [".", ",", "o", "H", "X", "*", "p", "s", "+"]

fig = plt.figure(figsize=(18,12))

i = 0

for sector in ipcc_sector:
    temp = df_prices_sect_wld.loc[df_prices_sect_wld.IPCC_cat_code==sector, :]
    plt.plot(temp.Year, temp.ecp_all_sectCO2_2019USD, 
             label=ipcc_sector_labels[sector],
             linewidth=2, marker=markers[i], ms=10)
    i+=1

#plt.title("Average world emissions price, by IPCC sector", fontsize=26)
plt.ylabel("2019 USD/tCO2", fontsize=24)
plt.yticks(size=18)
plt.xticks(size=18)

plt.xlim([1990, 2020])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, 
           shadow=False, ncol=3, fontsize=20)

plt.tight_layout()

plt.savefig("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/working_paper/figures/ecp_sect.pdf")

plt.close()
