# https://data.bis.org/topics/XRU/data

BISxRate = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/resources/data/WS_XRU_csv_col.csv")
colSel = [x for x in BISxRate.columns if len(x)==4 and x!="FREQ"]
colSel = colSel[180:]
rowSel = (BISxRate.FREQ=="A") & (BISxRate.COLLECTION=="A")

BISxRate = BISxRate.loc[rowSel, ["Reference area", "CURRENCY"]+colSel]

BISxRate.rename(columns={"CURRENCY":"currency_code", "Reference area":"jurisdiction"},
                inplace=True)

BISxRate = BISxRate.melt(id_vars=["jurisdiction", "currency_code"], 
                        var_name="year", value_name = "x-rate")

BISxRate.to_csv("/Users/gd/GitHub/ECP/_raw/wb_rates/xRate_bis.csv",
                index=None)