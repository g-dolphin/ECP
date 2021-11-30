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

cntries_list_II = ['Argentina',
                   'Denmark',
                   'Finland', 'Germany', 
                   'Mexico', 'Norway',
                   'Romania', 'Sweden',
                   'Switzerland', 'United Kingdom']


df_cov = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/data/coverage/total_coverage.csv")
df_cov = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/data/coverage/world_sectoral_coverage.csv")
df_cov_2010Scope = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/data/coverage/total_coverage_2010scope.csv")

df_prices_econ = pd.read_csv(user_root_path+git_repo_path+"/_dataset/price/ecp_economy/ecp.csv")
df_prices_sect = pd.read_csv(user_root_path+git_repo_path+"/_dataset/price/ecp_sectors/ecp_sector.csv")
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

plt.subplots(figsize=(30,34))
#ax=subplot(111)

cmap = sns.cm.rocket_r
#sns.set(font_scale=1)
ax = sns.heatmap(df_cov_hm, vmin=0, vmax=100, cmap=cmap, annot_kws={"size": 560},
                 cbar_kws={'label': '%'})

cax = plt.gcf().axes[-1]
cax.tick_params(labelsize=25)
ax.figure.axes[-1].yaxis.label.set_size(40)

#plt.title("Share of jurisdiction CO$_2$ emissions covered by carbon pricing mechanisms, by jurisdiction",
#          fontsize=26)

plt.xlabel("")
plt.xticks(rotation=45, size=26)
plt.yticks(size=26)
plt.ylabel("Jurisdiction", fontsize=32)

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

#plt.title("Share of world CO$_2$ emissions covered by carbon pricing mechanism, by sector",
#          fontsize=26)
plt.ylabel("IPCC source categories", fontsize=22)
plt.xlabel("")
plt.xticks(rotation=45, size=17)
plt.tight_layout()

plt.savefig(output_dir+"/cov_sect_hm.pdf")
plt.close()



## World coverage of schemes implemented as of 2010

jur_list_2010 = df_cov_2010Scope.loc[df_cov_2010Scope['cov_all_CO2_wldCO2']>0, "Jurisdiction"].unique() 

eu_ets_jur = ['Austria', 'Belgium', 'Bulgaria', 'Cyprus',
               'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France',
               'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy',
               'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands',
               'New Zealand', 'Norway', 'Poland', 'Portugal', 'Romania',
               'Slovak Republic', 'Slovenia', 'Spain', 'Sweden',
               'United Kingdom']

rggi_jur = ['Connecticut', 'Delaware', 'Maine', 'Maryland', 'Massachusetts', 
            'New Hampshire', 'New Jersey', 'New York', 'Rhode Island', 
            'Vermont']

df_cov_2010Scope = df_cov_2010Scope.loc[df_cov_2010Scope.Jurisdiction.isin(jur_list_2010), :]

df_cov_2010Scope_euets = df_cov_2010Scope.loc[df_cov_2010Scope.Jurisdiction.isin(eu_ets_jur), :].groupby(["Year"]).sum()
df_cov_2010Scope_euets.reset_index(inplace=True)
df_cov_2010Scope_euets["Jurisdiction"] = "EU ETS"
 
df_cov_2010Scope_rggi = df_cov_2010Scope.loc[df_cov_2010Scope.Jurisdiction.isin(rggi_jur), :].groupby(["Year"]).sum()
df_cov_2010Scope_rggi.reset_index(inplace=True)
df_cov_2010Scope_rggi["Jurisdiction"] = "RGGI"

df_cov_2010Scope = df_cov_2010Scope.loc[(~df_cov_2010Scope.Jurisdiction.isin(eu_ets_jur)) & (~df_cov_2010Scope.Jurisdiction.isin(rggi_jur)), :]
df_cov_2010Scope = pd.concat([df_cov_2010Scope, df_cov_2010Scope_euets, df_cov_2010Scope_rggi])

markers = [".", ",", "o", "H", "X", "*", "p", "s", "+"]



j = 0

for jur_group in [["EU ETS"], ["Alberta", "Switzerland", "RGGI"]]:
    i = 0
    
    fig = plt.figure(figsize=(18,12))
    
    for jur in jur_group:
        temp = df_cov_2010Scope.loc[df_cov_2010Scope.Jurisdiction==jur, :]
        plt.plot(temp.Year, temp.cov_all_CO2_wldCO2*100, 
                 label=jur,
                 linewidth=2, ms=10, marker=markers[i])
        i+=1
    
    plt.ylabel("% of world CO$_2$", fontsize=30)
    plt.yticks(size=28)
    plt.xticks(size=28)
    
    plt.xlim([2010, 2020])
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, 
               shadow=False, ncol=5, fontsize=30)
    
    plt.tight_layout()
    
    plt.savefig("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/working_paper/figures/wld_cov_2010scope_"+str(j)+".pdf")
    
    plt.close()
    
    j+=1


# PRICES

df_prices_econ = df_prices_econ.loc[df_prices_econ['Year']>=1990]
df_prices_econ = df_prices_econ.loc[df_prices_econ['Year']<=2020]

df_prices_sect = df_prices_sect.loc[df_prices_sect['Year']>=1990]
df_prices_sect = df_prices_sect.loc[df_prices_sect['Year']<=2020]


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

plt.savefig("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/working_paper/figures/price.pdf")

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

# Multi-sector time-series


sector_labels = {"ABFLOW003":"Power generation", 
                 "ABFLOW013":"Manufacturing", 
                 "ABFLOW028":"Road transport", 
                 "ABFLOW034":"Residential heating"}

iea_ipcc_map = {"ABFLOW003":"1A1A1", 
                 "ABFLOW013":"1A2I",
                 "ABFLOW028":"1A3B", 
                 "ABFLOW034":"1A4B"}

linestyle = ["solid", "dashed", "dotted", "dashdot", (0, (1,10)),
             (0, (5,10)), (0, (5,1)), (0, (3,5,1,5)), (0, (3,1,1,1)),
             (0, (3,1,1,1,1,1))]


fig, axs = plt.subplots(2,2, figsize=(30,24), sharey=True)

i = 0
j = 0

for sector in ["ABFLOW003", "ABFLOW013", "ABFLOW028", "ABFLOW034"]:
    print(i,j)
    temp = df_prices_sect.loc[(df_prices_sect.Jurisdiction.isin(cntries_list_II)) & (df_prices_sect.iea_code==sector)]
    temp = temp.loc[(temp.Year>=1990) & (temp.Year<=2020), :]
    temp_wld_sect = df_prices_sect_wld.loc[(df_prices_sect_wld.IPCC_cat_code==iea_ipcc_map[sector])]
    temp_wld_sect = temp_wld_sect.loc[(temp_wld_sect.Year>=1990) & (temp_wld_sect.Year<=2020), :]
    
    k=0
    for ctry in cntries_list_II:
        temp_ctry = temp.loc[temp.Jurisdiction==ctry]
        axs[i,j].plot(temp_ctry.Year, temp_ctry.total_ew_price_sector_2019USD, 
                 linewidth=2, label=ctry, color="royalblue", 
                 linestyle=linestyle[k])
        k+=1
    
   
    axwld = axs[i,j].twinx()
    axwld.plot(temp_wld_sect.Year, temp_wld_sect.ecp_all_sectCO2_2019USD, 
                  linestyle='-', color="indianred", 
                  linewidth=2.5)
    axwld.tick_params(colors='indianred', axis='y', labelsize=24)
    axwld.grid(False)
    axwld.set_ylim(0,6)
#    axwld.legend()
#    axwld.get_legend().remove()
    
#    plt.xlabel("")
    axs[i,j].set_xlim(1990,2020)
    axs[i,j].set_ylim(0,140)
    axs[i,j].set_title(sector_labels[sector], fontsize=42)
    axs[i,j].set_yticklabels(range(0,140,20), size=24, color="royalblue")
    axs[i,j].set_xticklabels(range(1990,2021,5), rotation=45, size=22)
    axs[i,j].set_ylabel("2019USD/tCO$_2$", size=28)
    
#    p = [axs[i,j], axwld]

    if i==0 and j==0:
        i=0
        j=1
    elif i==0 and j==1:
        i=1
        j=0
    elif i==1 and j==0:
        i=1
        j=1


#lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
#lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

#plt.legend(labels, fancybox=True,  bbox_to_anchor=(0.9, -0.15),
#           shadow=False, ncol=6, fontsize=24)

plt.tight_layout()

plt.savefig(output_dir+"/ecp_sector.pdf")
plt.close()


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
