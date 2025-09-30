"""Surface Soil Moisture Color Map.

Returns
-------
        Surface Soil Moisture Color Map : matplotlib.colors.LinearSegmentedColormap

"""

import matplotlib as mpl
import pandas as pd
from envrs.download_path import make_url


def load_cmap() -> mpl.colors.LinearSegmentedColormap:
    """Surface Soil Moisture Color Map.

    Loading Surface Soil Moisture Color Map based on the TU Wien standard.

    Parameters
    ----------
    None

    Returns
    -------
        Surface Soil Moisture Color Map : matplotlib.colors.LinearSegmentedColormap

    """

    def to_hex_str(x: list) -> str:
        """RGB Hex String.

        Convert RGB values to hex string

        Parameters
        ----------
        x : list
            RGB values

        Returns
        -------
        Hex string : str

        """
        return f"#{int(x.R):02x}{int(x.G):02x}{int(x.B):02x}"

    path = r"colour-tables%2Fssm-continuous.ct"
    color_df = pd.read_fwf(
        make_url(path, lfs="false", verbose=False), names=["R", "G", "B"], nrows=200
    )
    brn_yl_bu_colors = color_df.apply(to_hex_str, axis=1).to_list()
    return mpl.colors.LinearSegmentedColormap.from_list("", brn_yl_bu_colors)


SSM_CMAP = load_cmap()
