"""
Does not include any correction for under-reporting.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from settings import Settings

from src import utils
from src import paths
from src.standards import DataNames

country_list = ["Nigeria", "Ethiopia", "Congo, The Democratic Republic", 
                "South Africa", "Tanzania", "Kenya", "Sudan", "Algeria", "Uganda"]

def transform(x):
    """ Non-linear transform for y-axis """
    return np.cbrt(x)

# create the grid
n = len(country_list)
nx = 3
ny = int(np.ceil(n/nx))
gs = plt.GridSpec(ny, nx, wspace=0.4, hspace=0.5)


# load data
(inc_df, pop_df) = utils.get_datafiles(
    cases=Settings.cases, population=Settings.population
)

# lookup table
df = pd.merge(pop_df, inc_df, on=DataNames.iso)

axs = []
for ii, country in enumerate(country_list):

    # get country code
    iso = utils.get_country_code(country)

    # initialize the axes
    iy, ix = np.unravel_index(ii, (ny, nx))
    ax = plt.subplot(gs[iy, ix])
    axs.append(ax)

    years = np.arange(1974, 2023) 
    (cases, pop, time) = utils.get_cases_pop(iso, inc_df, pop_df, year=years)

    # calculate CV
    cv, cvt = utils.calc_cv(cases, time)
    print(f"{iso}")
    # print(f"CV year range: {cvt[0]} to {cvt[-1]}")
    # calculate MI
    mi, mit = utils.calc_wmi(cases, pop, time, start_year=years[0])
    # print(f"MI year range: {mit[0]} to {mit[-1]}")
    # trim mi to match cvt
    mi = mi[-len(cvt):]
    mit = mit[-len(cvt):]
    # print(f"trace starting in {mit[0]}")
    assert mit[0] == cvt[0]
    assert len(mit) == len(cvt)

    ax.plot(cv, transform(mi), '-k')
    ax.set_xlim(0, 4)
    # plt.ylim(-0.5, transform(1500))
    ax.set_ylim(transform(1), transform(4000))
    yticklabs = [100, 500, 1000, 2000, 4000]
    ytick = [transform(y) for y in yticklabs]
    ax.set_yticks(ytick, yticklabs)
    ax.set_title(iso)
    # ax.set_xlabel("CV")
    # ax.set_ylabel("Mean Incidence per 100,000")    


plt.gcf().tight_layout()
plt.savefig(f"{paths.figures}/S3.png", transparent=False)    