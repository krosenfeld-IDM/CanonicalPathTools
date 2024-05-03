import pandas as pd
import numpy as np

from src import paths
from src.standards import DataNames

"""
Clean the datasets.

Both the population and case data should be a country time series per row.
"""

from settings import Settings

def clean_incidence(filename, years):
    data = pd.read_csv(f"{paths.data}/{filename}")

    # Rename columns now
    col_map = {
        "Value": DataNames.cases,
        "SpatialDimValueCode": DataNames.iso,
        "Period": DataNames.year,
        "ParentLocationCode": DataNames.region,
        "Location": DataNames.country
    }
    data.rename(mapper=col_map, axis=1, inplace=True)
    # drop other columns
    drop_cols = [c for c in data.columns if c not in col_map.values()]
    data.drop(drop_cols, axis=1, inplace=True)

    # pivot on year
    data = data.pivot_table(
        index=[DataNames.iso, DataNames.region],
        columns=DataNames.year,
        values=DataNames.cases,
        fill_value=np.nan,
    ).reset_index()

    # drop years not in the range indicated by yeras
    year_range = [y for y in range(years[0], years[1]+1)]
    drop_years = [y for y in data.columns if y not in year_range]
    drop_years = [y for y in drop_years if y not in col_map.values()]
    data.drop(drop_years, axis=1, inplace=True)

    # save file
    data.to_csv(f"{paths.data}/{DataNames.cleaned}_{filename}", index=False)

def clean_population(filename, years):
    data = pd.read_csv(f"{paths.data}/{filename}", header=2)
    # rename columns
    col_map = {
        "Country Name": DataNames.country,
        "Country Code": DataNames.iso
        }
    for y in range(years[0], years[1]+1):
        col_map[str(y)] = y
    data.rename(mapper=col_map, axis=1, inplace=True)

   # drop years not in the range indicated by yeras
    year_range = [y for y in range(years[0], years[1]+1)]
    drop_years = [y for y in data.columns if y not in year_range]
    drop_years = [y for y in drop_years if y not in col_map.values()]
    data.drop(drop_years, axis=1, inplace=True)

    # save file
    data.to_csv(f"{paths.data}/{DataNames.cleaned}_{filename}", index=False)    


if __name__ == "__main__":
    # clean_incidence(Settings.cases, Settings.years)
    clean_population(Settings.population, Settings.years)
    print("done")
