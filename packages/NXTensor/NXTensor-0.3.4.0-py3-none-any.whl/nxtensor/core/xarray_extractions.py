#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 10:50:00 2020

@license : CeCILL-2.1
@author: sebastien@gardoll.fr
"""

from typing import Mapping, Union

import dask
import xarray as xr
import nxtensor.utils.coordinate_utils as coordinate_utils
from nxtensor.exceptions import ExtractionError
import numpy as np

# Ignore 'DataArray.py:1965: FutureWarning: dropping coordinates using `drop` is be deprecated; use drop_vars'
import warnings
warnings.filterwarnings('ignore')


def open_netcdf(netcdf_file_path: str, options: Mapping[str, str] = None) -> xr.Dataset:
    if options is None:
        options = {}
    return xr.open_dataset(netcdf_file_path, autoclose=True, lock=False, **options)


# Extract the region that centers the given lat/lon location.
def extract_square_region(dataset: xr.Dataset, variable_netcdf_attr_name: str, formatted_date: str,
                          lat: float, lat_resolution: float, y_size: int,
                          lon: float, lon_resolution: float, x_size: int,
                          lon_west_edge: float = -180., lon_east_edge: float = 180.,
                          variable_level: Union[int, slice] = None, level_netcdf_attr_name: str = 'level',
                          time_netcdf_attr_name: str = 'time',
                          lat_netcdf_attr_name: str = 'latitude',
                          lon_netcdf_attr_name: str = 'longitude',
                          has_to_round: bool = False, lat_nb_decimal: int = None, lon_nb_decimal: int = None,
                          dask_scheduler: str = 'single-threaded') -> np.ndarray:
    if has_to_round:
        if (not lat_nb_decimal) or (not lon_nb_decimal):
            raise ExtractionError("when has_to_round is true, lat_nb_decimal and lon_nb_decimal must be provided")
        lat = coordinate_utils.round_nearest(lat, lat_resolution, lat_nb_decimal)
        lon = coordinate_utils.round_nearest(lon, lon_resolution, lon_nb_decimal)

    if x_size % 2 == 1.:
        # Size dimension is odd => there is a true center and the given lat/lon will be the center of the extraction!
        half_lat_frame = ((y_size - 1) * lat_resolution) / 2.
        half_lon_frame = ((x_size - 1) * lon_resolution) / 2.
        # Upper bound is included.
        lat_min = lat - half_lat_frame
        lat_max = lat + half_lat_frame
        lon_min = lon - half_lon_frame
        lon_max = lon + half_lon_frame
    else:
        # Size dimension is even => there isn't any true center and the given lat/lon won't be the center of the
        # but the right bottom cell of the four cells that can be the center!
        # Upper bound is included.
        half_lat_frame = (y_size * lat_resolution) / 2.
        half_lon_frame = (x_size * lon_resolution) / 2.
        lat_min = (lat - half_lat_frame + lat_resolution)
        lat_max = (lat + half_lat_frame)
        lon_min = (lon - half_lon_frame)
        lon_max = (lon + half_lon_frame - lon_resolution)

    lat_series = dataset[lat_netcdf_attr_name]
    # Switching lat min and max.
    if lat_series[0] > lat_series[-1]:
        tmp = lat_min
        lat_min = lat_max
        lat_max = tmp
        del tmp

    indexers = dict()
    indexers[time_netcdf_attr_name] = formatted_date
    indexers[lat_netcdf_attr_name] = slice(lat_min, lat_max)
    if variable_level:
        indexers[level_netcdf_attr_name] = variable_level
    indexers[lon_netcdf_attr_name] = slice(lon_min, lon_max)

    with dask.config.set(scheduler=dask_scheduler):
        # Support extraction at the edge of the world, only for longitude!
        if lon_min < lon_west_edge or lon_max >= lon_east_edge:
            if lon_max >= lon_east_edge:
                lon_slice_left = slice(lon_min, lon_east_edge - lon_resolution)  # All included.
                lon_slice_right = slice(lon_west_edge, lon_max - lon_east_edge)  # All included.
            else: # lon_min < lon_west_edge
                lon_slice_left = slice(lon_east_edge + lon_min, lon_east_edge - lon_resolution)  # All included.
                lon_slice_right = slice(lon_west_edge, lon_max)  # All included.
            indexers[lon_netcdf_attr_name] = lon_slice_left
            left_data = dataset[variable_netcdf_attr_name].sel(indexers=indexers).compute().values
            indexers[lon_netcdf_attr_name] = lon_slice_right
            right_data = dataset[variable_netcdf_attr_name].sel(indexers=indexers).compute().values
            axis = len(left_data.shape) - 1
            result = np.concatenate((left_data, right_data), axis=axis)
        else:
            result = dataset[variable_netcdf_attr_name].sel(indexers=indexers).compute().values

        if np.isnan(result).max():
            print(f"> [WARNING] extracted region contains NaN (variable '{variable_netcdf_attr_name}' "
                  f"for indexers '{indexers}')")

        # As xarray stores lat before lon, so the result dimensions must be swapped, in order to get:
        # result shape: [levels,] x_size, y_size, because xarray shape: [levels,] lat/y_size, lon/x_size
        result = result.swapaxes(1, 2) if len(result.shape) > 2 else result.swapaxes(0, 1)
        return result


def __era5_unit_test_extraction(variable_name: str,
                                year: int, month: int, day: int, hour: int,
                                lat: float, lon: float,
                                variable_level: int = None) -> np.ndarray:
    from matplotlib import pyplot as plt

    # Era5 variable settings.
    y_size = 32
    x_size = y_size
    lat_resolution = 0.25
    lon_resolution = 0.25
    lat_nb_decimal = 2
    lon_nb_decimal = 2
    month_2_digit = f"{month:02d}"
    hour_2_digit = f"{hour:02d}"
    formatted_date = f'{year}-{month_2_digit}-{day}T{hour_2_digit}'
    if variable_level:
        netcdf_file_path = f'/bdd/ERA5/NETCDF/GLOBAL_025/4xdaily/AN_PL/{year}/{variable_name}.{year}{month_2_digit}' +\
            '.aphe5.GLOBAL_025.nc'
    else:
        netcdf_file_path = f'/bdd/ERA5/NETCDF/GLOBAL_025/hourly/AN_SF/{year}/{variable_name}.{year}{month_2_digit}' +\
            '.as1e5.GLOBAL_025.nc'

    print(f"> opening '{netcdf_file_path}'")
    with open_netcdf(netcdf_file_path) as dataset:
        print("> extracting region")
        extracted_region = extract_square_region(dataset=dataset, variable_netcdf_attr_name=variable_name,
                                                 formatted_date=formatted_date, variable_level=variable_level,
                                                 lat=lat, lat_resolution=lat_resolution, y_size=y_size,
                                                 lon=lon, lon_resolution=lon_resolution, x_size=x_size,
                                                 has_to_round=True, lat_nb_decimal=lat_nb_decimal,
                                                 lon_nb_decimal=lon_nb_decimal)
        print("> displaying region")
        plt.figure()
        plt.imshow(extracted_region, cmap='gist_rainbow_r', interpolation="none")
        plt.show()
        return extracted_region


def __test_simple_variable():
    variable_name = 'msl'
    year = 2000
    month = 10
    day = 1
    hour = 0
    lat = 39.7
    lon = 312  # Equivalent to -48 .
    return __era5_unit_test_extraction(variable_name, year, month, day, hour, lat, lon)


def __test_multilevel_variable():
    variable_name = 'ta'
    variable_level = 200
    year = 2011
    month = 8
    day = 25
    hour = 18
    lat = 26.5
    lon = 282.8  # Equivalent to -77.2 .
    return __era5_unit_test_extraction(variable_name, year, month, day, hour, lat, lon, variable_level)


def __all_tests():
    __test_simple_variable()
    __test_multilevel_variable()


if __name__ == '__main__':
    __all_tests()
