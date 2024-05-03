#!/usr/bin/env python
# coding: utf-8


import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# read in population
tmp = r'C:\Users\krosenfeld\OneDrive - Institute for Disease Modeling\Data\Population\WorldBank'
pop_df = pd.read_csv(os.path.join(tmp,'API_SP.POP.TOTL_DS2_en_csv_v2_673119.csv'), header=2)


# read in incidence
tmp = r'C:\Users\krosenfeld\OneDrive - Institute for Disease Modeling\Data\Incidence\WHO'
inc_df = pd.read_excel(os.path.join(tmp,'incidence_series.xls'), sheet_name='Measles')
inc_df.head()


# # Functions


def w(n,s=3,dx=2):
    """Gaussian function for weighting """
    x = np.arange(-n,0) + dx - 1
    return 1/(s*np.sqrt(2*np.pi)) * np.exp(-0.5*(x+dx)**2/s**2)


def calc_mean_incidence(cases, pop, pop_norm = 100000, ny=10):
    # check that number of cases and population are the same size
    assert cases.size == pop.size    
    # number of samples (years
    nx = len(cases)
    # make sure the we have enough samples
    assert nx >= ny
    # initialize array
    mi = np.zeros(nx-ny+1)
    # loop through calculation
    weights = w(ny)
    for ix in range(len(mi)):
        mi[ix] = pop_norm * np.sum(weights * cases[ix:(ix+ny)] / pop[ix:(ix+ny)]) / np.sum(weights)
    return mi


def calc_lcv(cases, pop, ny=10, pop_norm = 100000):
    """Local CV"""
    nx = len(cases)
    # initialize
    wcv = np.zeros(nx-ny)
    # weights
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


def calc_cv(cases, pop, ny=10, pop_norm =100000):
    """Weighted CV using LCV"""
    lcv = calc_lcv(cases, pop, ny=ny, pop_norm = pop_norm)
        
    cv = np.zeros(lcv.size)
    for ix in range(lcv.size):
        offset = np.min([ix+1, ny])
        weights = w(offset)
        cv[ix] = np.sum(weights*lcv[(ix-offset+1):ix+1])/np.sum(weights)
        
    return cv


def get_cases_pop(country,inc_df,pop_df):    
    Cname = country.capitalize()
    year = np.array([i for i in np.arange(1980,2019)])
    lind = inc_df.apply(lambda r: r['Cname'].startswith(Cname), axis=1)
    cases = np.array([inc_df[lind][str(y)].values[0] for y in year])
    pop = np.array([pop_df[pop_df['Country Name'] == Cname][str(y)].values[0] for y in year])
    return year, cases, pop


# # Fig S1
# mean incidence

# grab data
(year, cases, pop) = get_cases_pop('nigeria', inc_df, pop_df)

# make figure
plt.figure()
plt.plot(year,np.array(cases)/np.array(pop)*100000,'-o',markerfacecolor='gray', markeredgecolor='none')
plt.grid('on')
plt.ylabel('cases')
plt.xlabel('year')
xlim = plt.xlim()
plt.title('Nigeria')


plt.figure()
x = np.arange(1980,1991)
plt.plot(x,w(len(x)),'-o')
x = np.arange(1980,2011)
plt.plot(x,w(len(x)),'-o')
plt.xlim(xlim)
plt.grid('on')
plt.title('Nigeria')


plt.figure()
mean_incidence = calc_mean_incidence(cases,pop)
plt.plot(np.arange(1989,2019), mean_incidence, '-o')
plt.xlabel('time')
plt.ylabel('mean incidence per 100,000')
plt.ylim(bottom=0)
plt.grid('on')
plt.title('Nigeria')


# # Fig S2
# Coefficient of Variation (CV)

def calc_wcv(cases, pop, ny=10, pop_norm = 100000):
    """Weighted CV"""
    nx = len(cases)
    # initialize
    wcv = np.zeros(nx-ny)
    # weights
    weights = w(ny)
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



print('BOLIVIA')

(year, cases, pop) = get_cases_pop('bolivia', inc_df, pop_df)
plt.figure()
plt.plot(year,cases,'-o')
plt.xlabel('year')
plt.ylabel('cases');
plt.title('Bolivia')

# Note that this data looks a bit different than theirs! We have zero cases past 2001

wcv = calc_wcv(cases,pop)
plt.figure()
plt.plot(np.arange(1990,2019), wcv,'-o')
plt.xlabel('year')
plt.ylabel('CV (weighted)')
plt.ylim(bottom=0)
plt.grid('on')
plt.title('Bolivia')

lcv = calc_lcv(cases,pop)
plt.figure()
plt.plot(np.arange(1990,2019), lcv,'-o')
plt.xlabel('year')
plt.ylabel('CV (local)')
plt.ylim(bottom=0)
plt.grid('on')
plt.title('Bolivia')


# In[15]:


(year, cases, pop) = get_cases_pop('nigeria', inc_df, pop_df)

print('NIGERIA')

wcv = calc_lcv(cases,pop)
plt.figure()
plt.plot(np.arange(1990,2019), wcv,'-o')
plt.xlabel('year')
plt.ylabel('CV (local)')
plt.ylim(bottom=0)
plt.grid('on')
plt.title('Nigeria')

lcv = calc_cv(cases,pop)
plt.figure()
plt.plot(np.arange(1990,2019), lcv,'-o')
plt.xlabel('year')
plt.ylabel('CV ')
plt.grid('on')
plt.ylim([0.3, 1.5])
plt.title('Nigeria')

plt.show()
# In[ ]:




