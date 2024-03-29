import os
import numpy as np
import pandas as pd

def get_datafiles():
    """Returns Measles Incidence from WHO data file and country populations from pop_df

    Returns:
        inc_df, pop_df
    """
    # incidence
    tmp = r'C:\Users\krosenfeld\OneDrive - Institute for Disease Modeling\Data\Incidence\WHO'
    inc_df = pd.read_excel(os.path.join(tmp, 'incidence_series.xls'), sheet_name='Measles')

    # population
    # read in population
    tmp = r'C:\Users\krosenfeld\OneDrive - Institute for Disease Modeling\Data\Population\WorldBank'
    pop_df = pd.read_csv(os.path.join(tmp, 'API_SP.POP.TOTL_DS2_en_csv_v2_673119.csv'), header=2)

    return inc_df, pop_df

def get_data_lookup(inc_df,pop_df):
    """Return DF for matching country names and country codes between datasets"""
    # lookup table
    df = pd.merge(pop_df, inc_df, on='ISO_code')
    all_cols = df.columns
    keep_cols = {'Cname', 'ISO_code', 'WHO_Region', 'Country Name'}
    drop_cols = []
    for c in all_cols:
        if c not in keep_cols:
            drop_cols.append(c)
    df.drop(drop_cols, axis=1, inplace=True)
    return df

def calc_weights(n, s=3, dx=2):
    """Gaussian function for weighting """

    x = np.arange(-n, 0) + dx - 1
    return 1/(s*np.sqrt(2*np.pi)) * np.exp(-0.5*(x+dx)**2/s**2)

def calc_wmi(cases, pop, t, pop_norm = 100000, ny=10):
    """Calculate weighted mean incidence

    ny: number of data points / years to include in the calculation
    """

    # check that number of cases and population are the same size
    assert cases.size == pop.size
    # check that number of cases and years are the same size
    assert cases.size == t.size

    # number of samples
    nx = len(cases)
    # make sure the we have enough samples
    assert nx >= ny
    # initialize array
    mi = np.zeros(nx-ny+1)
    # loop through calculation
    weights = calc_weights(ny)

    for ix in range(len(mi)):
        mi[ix] = pop_norm * np.sum(weights * cases[ix:(ix+ny)] / pop[ix:(ix+ny)]) / np.sum(weights)

    t = t[(ny-1):]

    return mi, t

def calc_lcv(cases, pop, ny=10, pop_norm = 100000):
    """Local CV is equal weighted CV"""

    nx = len(cases)
    # initialize
    wcv = np.zeros(nx-ny+1)

    # weights (always use previous ny points)
    weights = np.ones(ny)

    for ix in range(len(wcv)):
        # data
        data = cases[ix:(ix+ny)] / pop[ix:(ix+ny)] * pop_norm

        # weighted mean incidence
        wmi = np.sum(weights * data) / np.sum(weights)

        # std
        num = np.sum(weights*(data - wmi)**2)
        nxp = np.sum(weights > 0)
        den = (nxp - 1) * np.sum(weights) / nxp

        # coefficient of variation is std / mean
        wcv[ix] = np.sqrt(num / den) / wmi

    return wcv


def calc_cv(cases, pop, t, ny=10, pop_norm=100000):
    """Weighted CV using Local CV"""

    # first calculate the local CV
    lcv = calc_lcv(cases, pop, ny=ny, pop_norm=pop_norm)

    # now go through and calculate weighted CV
    cv = np.zeros(lcv.size)
    for ix in range(lcv.size):
        # number of data points to include in the calculation
        offset = np.min([ix + 1, ny])
        # use gaussian weights
        weights = calc_weights(offset)
        # calculate CV
        cv[ix] = np.sum(weights * lcv[(ix - offset + 1):ix + 1]) / np.sum(weights)

    t = t[(ny-1):]

    return cv, t

def get_cases_pop(code, inc_df, pop_df, year = np.arange(1980, 2019)):
    """Retrieve the cases and population from the World Bank and WHO"""

    cases = [inc_df[inc_df['ISO_code'] == code][str(y)].values[0] for y in year]
    pop = [pop_df[pop_df['Country Code'] == code][str(y)].values[0] for y in year]

    # Cname = country.capitalize()
    # year =
    # lind = inc_df.apply(lambda r: r['Cname'].startswith(Cname), axis=1)
    # cases = np.array([inc_df[lind][str(y)].values[0] for y in year])
    # pop = np.array([pop_df[pop_df['Country Name'] == Cname][str(y)].values[0] for y in year])

    return np.array(cases), np.array(pop), np.array(year)