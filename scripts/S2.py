
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec

from settings import Settings

from src import utils
from src import paths
from src.standards import DataNames

ISO = 'BOL'

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

# add some cases in 2014...
cases[time == 2014] = 10

# create a gridspec with 4 rows and 1 column, the bottom row should be two panels
fig = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(4, 2)

ax0 = fig.add_subplot(gs[0, :])  # First row, span all columns
mask = (time >= 1981) & (time <= 2017)
ax0.plot(time[mask], cases[mask], '-o')
ax0.set_ylabel('cases'), ax0.set_xlabel('year')

ax1 = fig.add_subplot(gs[1, :])  # Second row, span all columns
ax2 = fig.add_subplot(gs[2, :])  # 3rd row, span all columns

############################

ISO = 'NGA'

# get case data
years = np.arange(1974, 2023) 
(cases, pop, time) = utils.get_cases_pop(ISO, inc_df, pop_df, year=years)

ax3_0 = fig.add_subplot(gs[3, 0])  # 3rd row, 1st column
cv, cvt = utils.calc_lcv(cases, time)
mask = (cvt >= 1990) & (cvt <= 2017)
ax3_0.plot(cvt[mask], cv[mask], '-o')
ax3_0.set_ylabel('CV')

ax3_1 = fig.add_subplot(gs[3, 1])  # 3rd row, 2nd column
cv, cvt = utils.calc_cv(cases, time)
mask = (cvt >= 1990) & (cvt <= 2017)
ax3_1.plot(cvt[mask], cv[mask], '-o')
ax3_1.set_ylabel('Mean CV')

fig.tight_layout()
plt.savefig(f"{paths.figures}/S2.png", transparent=False)