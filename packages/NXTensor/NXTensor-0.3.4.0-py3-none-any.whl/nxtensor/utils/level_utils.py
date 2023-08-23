from typing import Sequence

import xarray as xr


# Computes the level index of the targeted_level and applies the index offsets.
def create_slice(dataset: xr.Dataset, level_attr_name: str,  index_offsets: Sequence[int], targeted_level: int) -> slice:
    targeted_level_index = list(dataset[level_attr_name]).index(targeted_level)
    level_start = dataset[level_attr_name][index_offsets[0]+targeted_level_index]
    level_end = dataset[level_attr_name][index_offsets[1] + targeted_level_index]
    result = slice(level_start, level_end)
    return result
