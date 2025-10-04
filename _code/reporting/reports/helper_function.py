# Helper

def get_data_point(label, jurisdiction, year, config, dfs):
    meta = config['mappings'][label]
    if meta.get('static', False):
        return jurisdiction
    df = dfs[meta['file']]
    if 'jurisdiction' in df.columns:
        df = df[df['jurisdiction'] == jurisdiction]
    if 'year' in df.columns and year is not None:
        df = df[df['year'] == year]
    col = meta['column']
    op = meta['operation']
    if op == 'mean':
        return df[col].mean()
    elif op == 'max':
        return df[col].max()
    elif op == 'sum':
        return df[col].sum()
    elif op == 'list':
        df = df[(~df['tax_curr_code'].isna()) | (~df['ets_curr_code'].isna())]
        return df[col].dropna().unique().tolist()
    elif op == 'percent_global':
        total = df[col].sum()
        grand_total = dfs[meta['file']][col].sum()
        return 100 * total / grand_total
    elif op == 'count_unique':
        return df[df[col] == meta['filter_value']]['jurisdiction'].nunique()
    elif op == 'count_both':
        counts = dfs[meta['file']].groupby('jurisdiction')[col].nunique()
        return counts[counts >= 2].count()
    elif op == 'passthrough':
        return df[col].iloc[0] if not df.empty else None
    else:
        raise ValueError(f"Unknown op {op}")