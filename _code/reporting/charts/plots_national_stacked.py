from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
import pandas as pd


PathLike = Union[str, Path]


def plot_stacked_national_bar(
    df: pd.DataFrame,
    output_plot_path: PathLike,
    output_data_path: PathLike,
) -> None:
    """
    Stacked bar chart for national jurisdictions.

    Parameters
    ----------
    df : DataFrame
        Input table for national stack (whatever structure you already use).
    output_plot_path : str or Path
        Path for figure.
    output_data_path : str or Path
        Path for underlying data CSV.
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    # existing plotting code here
    # ...
    fig.tight_layout()

    output_plot_path = Path(output_plot_path)
    output_plot_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_plot_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    output_data_path = Path(output_data_path)
    output_data_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_data_path, index=False)
