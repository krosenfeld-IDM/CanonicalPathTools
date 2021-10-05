#!/usr/bin/env python
# coding: utf-8


import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('..'))
import utils


# load data
(inc_df, pop_df) = utils.get_datafiles()


# rename column to match
tmp = pop_df
tmp = pop_df.rename({'Country Code': 'ISO_code'}, axis=1)
# lookup table 
df = pd.merge(tmp, inc_df, on='ISO_code')
all_cols = df.columns
keep_cols = {'Cname', 'ISO_code', 'WHO_REGION', 'Country Name'}
drop_cols = []
for c in all_cols:
    if c not in keep_cols:
        drop_cols.append(c)
df.drop(drop_cols,axis=1,inplace=True)
df.head()


# https://apps.who.int/medicinedocs/en/d/Js2297e/2.html
# EMR: Eastern Mediterranean, AFR: African, EUR: European, SEAR: South-East Asia, WPR: Western Pacific, AMR: Americas
df['WHO_REGION'].unique()


# loop through ISO code and calculate mean incidence and CV for specific year
years = [1990, 2014]
regions = ['AMR', 'AFR']
# years = [1990]
# regions = ['AMR']
res_dict = {}
# loop over regions
for region in regions:
    res_dict.update({region:{}})
    df_ = df[df['WHO_REGION'] == region]
    res = {}
    cname = []
    # loop over countries in the region
    for index,row in df_.iterrows():
        # country name by ISO code
        cname.append(row['ISO_code'])
        # get the data
        (cases,pop,time) = utils.get_cases_pop(row['ISO_code'], inc_df, pop_df)
        # calculate CV
        cv, cvt = utils.calc_cv(cases, pop, time)
        # calculate MI
        mi, mit = utils.calc_wmi(cases, pop, time)
        for y in years:
            if str(y)+'_cv' not in res.keys():
                res.update({str(y)+'_cv':list(cv[cvt == y])})
                res.update({str(y)+'_mi':list(mi[mit == y])})
            else:
                res[str(y)+'_cv'].append(cv[cvt == y][0])
                res[str(y)+'_mi'].append(mi[mit == y][0])
    # save dictionary by region
    res.update({'ISO_code':cname})
    res_dict[region] = pd.DataFrame.from_dict(res)


# make figures

afr_col = 'green'
amr_col = 'purple'
ms = 50
plt.figure(figsize=(10,8))
plt.scatter(res_dict['AFR']['1990_cv'],res_dict['AFR']['1990_mi'],
            ms,marker='o',edgecolor=afr_col,facecolors='none',label='Africa 1990')
plt.scatter(res_dict['AFR']['2014_cv'],res_dict['AFR']['2014_mi'],
            ms,marker='o',edgecolor=afr_col,facecolors=afr_col,label='Africa 2014')
plt.scatter(res_dict['AMR']['1990_cv'],res_dict['AMR']['1990_mi'],
            ms,marker='o',edgecolor=amr_col,facecolors='none',label='Americas 1990')
plt.scatter(res_dict['AMR']['2014_cv'],res_dict['AMR']['2014_mi'],
            ms,marker='o',edgecolor=amr_col,facecolors=amr_col,label='Americas 2014')

# plt.yscale('log')
plt.xlabel('CV')
plt.ylabel('Mean Incidence per 100,000')
# plt.legend()
ax = plt.gca()
ax.legend(loc='upper left', bbox_to_anchor= (1.01, 1), ncol=2, 
            borderaxespad=0, frameon=False)
plt.savefig('Fig1.png',transparent=True)






