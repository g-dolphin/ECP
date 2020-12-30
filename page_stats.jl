
Pkg.activate()

Pkg.add("UrlDownload")
Pkg.add("DataFrames")
Pkg.add("PyCall")

using DataFrames
using CSV
using PyPlot
using PyCall

#if you want to keep the Python True/False syntax
#const True = true
#const False = false

countries_regex = r"Belgium|Chile|France|Germany|Norway|Sweden|World"
countries_list = ["Belgium", "Chile", "France", "Germany", "Norway", "Sweden", "World"]
colors = ["teal", "lightseagreen", "skyblue", "steelblue", "olivedrab", "forestgreen", "cornflowerblue"]

# ## Time series
# ### Coverage

#raw_data = urldownload("https://raw.githubusercontent.com/gd1989/ECP/master/Total_economy/Coverage/Total_coverage.csv?token=AD3IRDAVNXIUQ6ER3UJU5WS7UQL5K")
path_cov = "/Users/GD/Documents/GitHub/ECP/Total_economy/Coverage/Total_coverage.csv"

coverage = CSV.read(path_cov, DataFrame)
select!(coverage, ["Jurisdiction", "Year", "cov_tax_ets_share_jurGHG"])

coverage.cov_perc = coverage.cov_tax_ets_share_jurGHG*100

figure(figsize=(12, 10))

i = 1
for ctry in countries_list
        temp = coverage[coverage[:, :Jurisdiction] .== ctry, :]
        plot(temp.Year, temp.cov_perc, color=colors[i], label=ctry)
        global i += 1
end

xlabel("Time", fontsize=14)
ylabel("Coverage (% GHG)", fontsize=14)
yticks(fontsize=12)
xlim(1990, 2016)
ylim(0)
legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox=true, shadow=true, ncol=4, fontsize=14)
plt.tight_layout()

plt.savefig("/Users/GD/Documents/GitHub/ECP/page/_assets/coverage_ts.png")
plt.close()

# ### ECP
path_ecp = "/Users/GD/Documents/GitHub/ECP/Total_economy/ECP_fixed_weights/ecp_2015.csv"

ecp = CSV.read(path_ecp, DataFrame)

figure(figsize=(12, 10))

i = 1
for ctry in countries_list
        temp = ecp[ecp[:, :Jurisdiction] .== ctry, :]
        plot(temp.Year, temp.ECP_tax_ets_jurGHG_2019USD, color=colors[i], label=ctry)
        global i += 1
end

xlabel("Time", fontsize=14)
ylabel("Carbon price (2019USD/tCO2)", fontsize=14)
yticks(fontsize=12)
xlim(1990, 2018)
ylim(0)

legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox=true, shadow=true, ncol=4, fontsize=14)
plt.tight_layout()

plt.savefig("/Users/GD/Documents/GitHub/ECP/page/_assets/ecp_ts.png")
plt.close()

# ## Distribution
# ### Distribution of coverage in 2016

cov_2016 = coverage[coverage[:Year] .== 2016, :]
dropmissing!(cov_2016)


fig, (ax, ax2) = plt.subplots(2,1, sharex=true) # make the axes

ax.hist(cov_2016.cov_tax_ets_share_jurGHG, color="blue", edgecolor="white",
        bins=20,
        density=false, alpha=0.5)
ax2.hist(cov_2016.cov_tax_ets_share_jurGHG, color="blue", edgecolor="white",
         bins=20,
         density=false, alpha=0.5)

ax.set_ylim([150,170]) # numbers here are specific to this example
ax2.set_ylim([0,10]) # numbers here are specific to this example

ax.spines["bottom"].set_visible(false)
ax2.spines["top"].set_visible(false)

ax.xaxis.tick_bottom()
ax.tick_params(labeltop=false)
ax2.xaxis.tick_bottom()

#plt.axvline(mean_age, label = "Mean", color = "red")
#plt.axvline(median_age, label = "Median")

plt.legend()

plt.savefig("/Users/GD/Documents/GitHub/ECP/page/_assets/coverage_hist.png")
plt.close()
