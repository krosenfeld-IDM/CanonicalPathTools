#!/usr/bin/env python
# coding: utf-8


import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from settings import Settings

from src import utils
from src import paths
from src.standards import DataNames

# load data
(inc_df, pop_df) = utils.get_datafiles(
    cases=Settings.cases, population=Settings.population
)


# rename column to match
# tmp = pop_df
# tmp = pop_df.rename({"Country Code": "ISO3"}, axis=1)
# inc_df = inc_df.rename(
#     {"SpatialDimValueCode": "ISO3", "ParentLocationCode": "Region"}, axis=1
# )
# lookup table
df = pd.merge(pop_df, inc_df, on=DataNames.iso)
# all_cols = df.columns
# keep_cols = {"Cname", "ISO3", "Region", "Country Name"}
# drop_cols = []
# for c in all_cols:
#     if c not in keep_cols:
#         drop_cols.append(c)
# df.drop(drop_cols, axis=1, inplace=True)
df.head()


# https://apps.who.int/medicinedocs/en/d/Js2297e/2.html
# EMR: Eastern Mediterranean, AFR: African, EUR: European, SEAR: South-East Asia, WPR: Western Pacific, AMR: Americas
df[DataNames.region].unique()


# loop through ISO code and calculate mean incidence and CV for specific year
years = [1990, 2014]
regions = ["AMR", "AFR"]
# years = [1990]
# regions = ['AMR']
res_dict = {}
# loop over regions
for region in regions:
    res_dict.update({region: {}})
    df_ = df[df[DataNames.region] == region].drop_duplicates()
    res = {}
    cname = []
    # loop over countries in the region
    for index, row in df_.iterrows():
        try:
            # country name by ISO code
            cname.append(row[DataNames.iso])
            # get the data
            (cases, pop, time) = utils.get_cases_pop(row[DataNames.iso], inc_df, pop_df)
            # calculate CV
            cv, cvt = utils.calc_cv(cases, pop, time)
            # calculate MI
            mi, mit = utils.calc_wmi(cases, pop, time)
            for y in years:
                if str(y) + "_cv" not in res.keys():
                    res.update({str(y) + "_cv": list(cv[cvt == y])})
                    res.update({str(y) + "_mi": list(mi[mit == y])})
                else:
                    res[str(y) + "_cv"].append(cv[cvt == y][0])
                    res[str(y) + "_mi"].append(mi[mit == y][0])
        except Exception as e:
            raise e
        
    # save dictionary by region
    res.update({DataNames.iso: cname})
    res_dict[region] = pd.DataFrame.from_dict(res)


# make figures

afr_col = "green"
amr_col = "purple"
ms = 50
plt.figure(figsize=(10, 8))
plt.scatter(
    res_dict["AFR"]["1990_cv"],
    res_dict["AFR"]["1990_mi"],
    ms,
    marker="o",
    edgecolor=afr_col,
    facecolors="none",
    label="Africa 1990",
)
plt.scatter(
    res_dict["AFR"]["2014_cv"],
    res_dict["AFR"]["2014_mi"],
    ms,
    marker="o",
    edgecolor=afr_col,
    facecolors=afr_col,
    label="Africa 2014",
)
plt.scatter(
    res_dict["AMR"]["1990_cv"],
    res_dict["AMR"]["1990_mi"],
    ms,
    marker="o",
    edgecolor=amr_col,
    facecolors="none",
    label="Americas 1990",
)
plt.scatter(
    res_dict["AMR"]["2014_cv"],
    res_dict["AMR"]["2014_mi"],
    ms,
    marker="o",
    edgecolor=amr_col,
    facecolors=amr_col,
    label="Americas 2014",
)

# plt.yscale('log')
plt.xlim(-0.1, 3.2)
plt.ylim(0, 1500)
plt.xlabel("CV")
plt.ylabel("Mean Incidence per 100,000")
# plt.legend()
ax = plt.gca()
ax.legend(
    loc="upper left", bbox_to_anchor=(1.01, 1), ncol=2, borderaxespad=0, frameon=False
)
plt.gcf().tight_layout()
plt.savefig(f"{paths.scripts}/Fig1.png", transparent=False)
