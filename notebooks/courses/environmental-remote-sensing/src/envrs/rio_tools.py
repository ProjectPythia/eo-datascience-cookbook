# ruff: noqa: ANN D100
import pandas as pd
import rasterio as rio
from rasterio import windows
from shapely import box


def clipped_read(entries, location):
    if isinstance(entries, pd.Series):
        entries = entries.to_dict()
    elif isinstance(entries, dict):
        pass
    else:
        err = f"entries must be a pandas series or a dictionary, not {type(entries)}"
        raise TypeError(err)

    # Retrieve the content of the rasters
    array_pairs, profile_pairs, tag_pairs = {}, {}, {}
    for raster_name, raster_path in entries.items():
        with rio.open(raster_path) as raster:
            # Set the profile
            profile = raster.profile

            # Set the shared extent
            naive_bounds = box(*location.to_crs(profile["crs"]).total_bounds)
            raster_bounds = box(*raster.bounds)
            shared_bounds = raster_bounds.intersection(naive_bounds).bounds

            # Set the clipping window, and update the profile
            window = windows.from_bounds(*shared_bounds, profile["transform"])
            window = window.round()
            profile["transform"] = windows.transform(window, profile["transform"])
            profile["height"] = window.height
            profile["width"] = window.width

            # Do a PARTIAL reading, set profiles and tags
            array_pairs[raster_name] = raster.read(1, window=window)

            profile_pairs[raster_name] = pd.Series(profile)
            tag_pairs[raster_name] = pd.Series(raster.tags())

    # Concatenate the profiles and the tags
    profile_frame = pd.concat(profile_pairs, axis=1).T
    tag_frame = pd.concat(tag_pairs, axis=1).T
    return array_pairs, profile_frame, tag_frame


def write_raster(array_pairs, profile_frame, tag_frame, raster_path):
    # Check for duplicate entries on the profiles
    nunique_profiles = profile_frame.nunique(axis=0)
    several_profiles = nunique_profiles > 1
    if several_profiles.any():
        offending_entries = nunique_profiles[several_profiles].index.tolist()
        err = f"{offending_entries} have several possible values"
        raise RuntimeError(err)

    # make the output profile and update
    out_profile = profile_frame.drop_duplicates().iloc[0].to_dict()
    out_profile["count"] = len(array_pairs)

    # keep only tags where the count is larger than one
    nunique_tags = tag_frame.nunique(axis=0)
    relevant_tags = nunique_tags[nunique_tags == 1].index.tolist()
    tags = tag_frame[relevant_tags].drop_duplicates().iloc[0].to_dict()

    # Write the output file
    with rio.open(raster_path, "w", **out_profile) as out_raster:
        # update the scales and offsets
        if "add_offset" in tag_frame.columns:
            out_raster.offsets = tag_frame["add_offset"].astype(float)

        if "scale_factor" in tag_frame.columns:
            out_raster.scales = tag_frame["scale_factor"].astype(float)

        # Update the tags
        out_raster.update_tags(**tags)

        # Iteratively write each band and its description
        for band_idx, (band_name, band_data) in enumerate(array_pairs.items(), 1):
            out_raster.write(band_data, band_idx)
            out_raster.set_band_description(band_idx, band_name)
