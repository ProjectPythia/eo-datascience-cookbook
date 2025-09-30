# ruff: noqa: ANN D100 PD010

import re
from datetime import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr


def extract_extra_attrs(granule):
    att_pairs = {}
    for att in dict(granule.items())["umm"]["AdditionalAttributes"]:
        att_name, att_values = att["Name"], att["Values"]
        if len(att_values) == 1:
            att_pairs[att_name] = att_values[0]

    return att_pairs


def tabulate_hls_uris(iterable):
    uri_pile, info_pile, name_pile = [], [], []
    for product_uri in iterable:
        # Set the uri
        uri_pile.append(product_uri)

        # process the stem
        if isinstance(product_uri, Path):
            stem = product_uri.stem
        elif isinstance(product_uri, str):
            stem = product_uri.split("/")[-1].replace(".tif", "")
        else:
            err = (
                "the contens of iterable should be 'str' or Path, "
                f"not {type(product_uri)}"
            )
            raise TypeError(err)
        stem_info = stem.split(".")

        # Alter the stem to avoid issues induced by the dot within the version
        stem_info.insert(3, stem_info.pop(1))
        version = f"{stem_info[4]}.{stem_info[5]}"
        stem_info[4] = version
        stem_info.pop(5)

        # Append the info and the new name
        info_pile.append(stem_info)
        name_pile.append("_".join(stem_info[:-1]))

    # Place the information on a dataframe
    columns = ["product", "tile", "time", "sensor", "version", "suffix"]
    uri_frame = pd.DataFrame(info_pile, index=uri_pile, columns=columns).reset_index(
        names="uri"
    )

    # Add the name, clean up the suffix, sort, and return
    uri_frame["stem"] = name_pile
    uri_frame["suffix"] = uri_frame["suffix"].replace("B8A", "B08A")
    return uri_frame.sort_values(["stem", "suffix"], ascending=True)


def harmonize_hls_frame(uri_frame):
    # Set the column renames
    common_bands = {
        "B01": "CoastalAerosol",
        "B02": "Blue",
        "B03": "Green",
        "B04": "Red",
    }
    landsat_bands = {**common_bands, "B05": "NIRnarrow", "B06": "SWIR1", "B07": "SWIR2"}
    sentinel_bands = {
        **common_bands,
        "B08A": "NIRnarrow",
        "B11": "SWIR1",
        "B12": "SWIR2",
    }

    # Separate by sensor, drop non-shared bands, rename
    landsat_frame = (
        uri_frame[uri_frame["sensor"] == "L30"]
        .pivot(index="stem", columns="suffix", values="uri")
        .drop(columns=["B09", "B10", "B11"])
        .rename(columns=landsat_bands)
    )
    sentinel_frame = (
        uri_frame[uri_frame["sensor"] == "S30"]
        .pivot(index="stem", columns="suffix", values="uri")
        .drop(columns=["B05", "B06", "B07", "B08", "B09", "B10"])
        .rename(columns=sentinel_bands)
    )

    # Concatenate and return
    return pd.concat([landsat_frame, sentinel_frame], axis=0).sort_index()


def att2time(att):
    if (";" in att) or ("+" in att):
        split_time = re.split(r"\s?[\+\;]\s", att)
        start, end = [dt.fromisoformat(s[:-1]) for s in split_time]
        time = start + (end - start) / 2
    else:
        time = dt.fromisoformat(att[:-1])
    return time


def preprocess_fmask(fmask):
    debanded = fmask["band_data"]
    bits = xr.apply_ufunc(
        np.unpackbits,
        debanded,
        input_core_dims=[["band", "y", "x"]],
        output_core_dims=[["flag", "y", "x"]],
        exclude_dims=set(["band"]),  # noqa: C405
        keep_attrs=True,
        kwargs={"axis": 0},
        dask="allowed",
    )

    # Convert the flags to bool, set the names
    flags = bits.sel(flag=slice(2, 9)).astype(bool)
    flags["flag"] = [
        "water",
        "snow or ice",
        "cloud shadow",
        "adjacent to cloud",
        "cloud",
        "cirrus cloud",
    ]
    flags.name = "masks"

    # Convert the aerosol data, set the name
    aerosol_parts = bits.sel(flag=slice(0, 2))
    aerosol = aerosol_parts.sel(flag=1) + 10 * aerosol_parts.sel(flag=0)
    aerosol.name = "aerosol"

    # set the time
    time = att2time(debanded.attrs["SENSING_TIME"])
    return xr.merge([flags, aerosol]).expand_dims({"time": [time]}, axis=0)


def preprocess_bands(bands):
    # Set the band names
    renames = {}
    for var_name in bands:
        renames[var_name] = bands[var_name].attrs["long_name"]

    # Set the time
    time = att2time(bands.attrs["SENSING_TIME"])
    return bands.rename_vars(renames).expand_dims({"time": [time]})
