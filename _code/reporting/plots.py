import matplotlib.pyplot as plt

def plot_coverage(df, output_dir):
    latest_year = df['Year'].max()
    coverage = df[df['Year'] == latest_year].groupby('Country')['Emissions'].sum().reset_index()
    coverage = coverage.sort_values(by='Emissions', ascending=False)

    plt.figure(figsize=(12,6))
    plt.bar(coverage['Country'], coverage['Emissions'])
    plt.xticks(rotation=90)
    plt.title(f'Coverage by Country - {latest_year}')
    plt.xlabel('Country')
    plt.ylabel('MtCO₂')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/coverage_by_country.png")
    plt.close()
