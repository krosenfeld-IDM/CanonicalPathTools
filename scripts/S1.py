
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec

from settings import Settings

from src import utils
from src import paths
from src.standards import DataNames

ISO = 'NGA'

# set the fontsize for matplotlib to 16
plt.rcParams.update({"font.size": 10})

# load data
(inc_df, pop_df) = utils.get_datafiles(
    cases=Settings.cases, population=Settings.population
)

# lookup table
df = pd.merge(pop_df, inc_df, on=DataNames.iso)

# get case data
years = np.arange(1974, 2023) 
(cases, pop, time) = utils.get_cases_pop(ISO, inc_df, pop_df, year=years)

# calculate WMI
wmi, wmit = utils.calc_wmi(cases, pop, time, start_year=years[0])

# create gridspec with 3 rows and 1 column
fig = plt.figure(figsize=(5, 10))
gs = gridspec.GridSpec(3, 1)

# subplot A: plot incidence
ax0 = plt.subplot(gs[0])
mask = (time >= 1981) & (time <= 2017)
ax0.plot(time[mask], cases[mask] / pop[mask] * 100000, '-o')
ax0.set_ylabel('incidence per 100k')
ax0.set_ylim(0, None)

ax1 = plt.subplot(gs[1])
start_year = 1980
years = [1990, 2010]
for year in years:
    n = year - start_year + 1
    w = utils.calc_weights(n)
    ax1.plot(np.arange(start_year, year+1), w, '-o')

# subplot C: plot WMI
ax2 = plt.subplot(gs[2])
mask = (wmit >= 1990) & (wmit <= 2017)
ax2.plot(wmit[mask], wmi[mask], '-o')
ax2.set_ylabel('mean incidence per 100k')
ax2.set_ylim(0, None)

fig.tight_layout()
plt.savefig(f"{paths.figures}/S1.png", transparent=False)