# Load data
file_path = "/Users/gd/OneDrive - rff/Documents/Research/resources/data/WS_XRU_csv_col.csv"
output_path = "/Users/gd/GitHub/ECP/_raw/wb_rates/xRate_bis.csv"

# Read and filter data
df = pd.read_csv(file_path)
year_cols = [col for col in df.columns if col.isdigit() and col != "FREQ"][180:]
df_filtered = df[(df["FREQ"] == "A") & (df["COLLECTION"] == "A")]

# Select and rename columns
df_filtered = df_filtered[["Reference area", "CURRENCY"] + year_cols]
df_filtered.rename(columns={"Reference area": "jurisdiction", "CURRENCY": "currency_code"}, inplace=True)

# Reshape and export
df_melted = df_filtered.melt(id_vars=["jurisdiction", "currency_code"], 
                             var_name="year", value_name="x-rate")
df_melted.to_csv(output_path, index=False)
