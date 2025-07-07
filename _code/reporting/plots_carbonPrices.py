import matplotlib.pyplot as plt

def plot_carbon_prices(df, output_dir):
    grouped = df.groupby('Year')['Price'].mean().reset_index()
    plt.figure(figsize=(10,6))
    plt.plot(grouped['Year'], grouped['Price'], marker='o')
    plt.title('Average Carbon Price')
    plt.xlabel('Year')
    plt.ylabel('USD/tCO₂')
    plt.grid(True)
    plt.savefig(f"{output_dir}/avg_carbon_price.png")
    plt.close()
