#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib as mpl
import compare_hists
import pandas as pd
import json
import argparse
import sys


## make it require at least 2 arguments (json file, subsystem name) and optional argument of ....black list????????? idk
parser = argparse.ArgumentParser()
parser.add_argument(
    "jsonfile", type=str, help="path to JSON file containing data:ref pairs"
)
parser.add_argument(
    "subsystem", type=str, help="subsystem configuration to use. Example CSC or EMTF"
)
parser.add_argument(
    "--blacklist",
    type=str,
    help="path to JSON file containing list of black listed hists",
    default=None,
    required=False
)


args = parser.parse_args()

## these are just to pad out the compare_hist.process() function. We don't actually use these information
config_dir = "../config"
data_series = "Run2018"
data_sample = "SingleMuon"
ref_series = "Run2018"
ref_sample = "SingleMuon"
chunk_index = 0
chunk_size = 9999
dqmSource = "Offline"


datadict = json.load(open(args.jsonfile))
subsystem = args.subsystem


## create the csv files for storing the scores
from pathlib import Path

Path("csv").mkdir(parents=True, exist_ok=True)
Path("tmp").mkdir(parents=True, exist_ok=True)
with open("tmp/beta_binomial.csv", "w+") as myfile:
    myfile.write(
        "histname,bb_pull,bb_chi2,ref_run,data_run\n"
    )
with open("tmp/ks.csv", "w+") as myfile:
    myfile.write(
        "histname,ks,ref_run,data_run\n"
    )
with open("tmp/pullvals.csv", "w+") as myfile:
    myfile.write(
        "histname,maxpull,chi2,ref_run,data_run\n"
    )

## for storing plots with weights
# with open("histWWeights.csv", "a+") as myfile:
#     myfile.write("histname\n")



## take a list of runs and look for UL
production = "UL"
primary_dataset = "SingleMuon"


for data_path in datadict:
    runnum_idx = data_path.find("_R000") + 5  # data_path[-11:-5]
    data_run = data_path[runnum_idx : runnum_idx + 6]
    ref_path = datadict[data_path]
    runnum_idx = ref_path.find("_R000") + 5
    ref_run = ref_path[runnum_idx : runnum_idx + 6]
    compare_hists.process(
        chunk_index,
        chunk_size,
        config_dir,
        dqmSource,
        subsystem,
        data_series,
        data_sample,
        data_run,
        data_path,
        ref_series,
        ref_sample,
        ref_run,
        ref_path,
        output_dir="./out/",
        plugin_dir="../plugins/",
    )

bb = pd.read_csv("tmp/beta_binomial.csv")
pv = pd.read_csv("tmp/pullvals.csv")
ks = pd.read_csv("tmp/ks.csv")

## find a way to merge with the data sum, data avg, data std correctly, or maybe remove them all together since it might not be useful
mergekw = {
    "how": "outer",
    "on": ["histname", "data_run", "ref_run"],
}  # "data_sum", "data_avg", "data_std", "ref_sum", "ref_avg", "ref_std"]}


## need to think about how to use the blacklist?
## remove the blacklisted rows before saving the csv? remove the blacklisted rows before making the plots?
## probably can remove the blacklisted plots from the merged df

## i think also print the 95 percentile number for each test
## use the merged df and not the 1d/2d so that betabinomial isn't split into 2 number


merged = bb.merge(pv, **mergekw)
merged = merged.merge(ks, **mergekw)

merged.to_csv(f"csv/{subsystem}.csv")

## take the merged1d and merged2d out of the try except thing, then can check if any of them are empty and run the code accordingly
## should also be saving the beta-binomial, ks, pullvals.csv in another folder. maybe make a tmp folder


try:
    merged1d = merged[~np.isnan(merged.ks)]
    fig, ax = plt.subplots(3)
    ax[0].hist(merged1d.ks)
    ax[0].set_title(f"{subsystem} ks, beta-binom pull, beta-binom chi2")
    ax[1].hist(np.absolute(merged1d.bb_pull), bins=20)
    _, bins, _ = ax[2].hist(merged1d.bb_chi2, bins=21, range=(0, 105))
    xlabels = ax[2].get_xticks().tolist()
    xlabels = [str(x) for x in xlabels[0:-1]]
    xlabels[-1] += "+"
    ax[2].set_xticklabels(xlabels)
    fig.savefig(f"plots/ks_{subsystem}.png", bbox_inches="tight")
except:
    pass

## 2d
try:
    merged2d = merged[~np.isnan(merged.maxpull)]

    ## maybe using numpy.hist would work better which allow bar
    Path("plots").mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots()
    xmax = 37
    histkwarg = {"bins": 20, "alpha": 0.5, "range": (0, xmax)}
    ax.hist(
        np.clip(np.absolute(merged2d.maxpull), a_min=None, a_max=xmax),
        label="max_pull",
        **histkwarg,
    )
    _, bins, _ = ax.hist(
        np.absolute(merged2d.bb_pull), label="beta_binomial", **histkwarg
    )
    xlabels = ax.get_xticks().tolist()
    xlabels = [str(x) for x in xlabels[0:-1]]
    xlabels[-1] += "+"
    ax.set_xticklabels(xlabels)
    ax.set_title(f"{subsystem} pull values and beta-binomial")
    ax.legend()
    fig.savefig(f"plots/pullvals_{subsystem}.png", bbox_inches="tight")

    fig2, ax2 = plt.subplots()
    xmax = 105
    histkwarg = {"bins": 21, "alpha": 0.5, "range": (0, xmax)}
    ax2.hist(np.clip(merged2d.chi2, a_min=None, a_max=xmax), label="chi2", **histkwarg)
    _, bins, _ = ax2.hist(
        np.clip(merged2d.bb_chi2, a_min=None, a_max=xmax),
        label="beta_binomial chi2",
        **histkwarg,
    )
    xlabels = ax2.get_xticks().tolist()
    xlabels = [str(x) for x in xlabels[0:-1]]
    xlabels[-1] += "+"
    ax2.set_xticklabels(xlabels)
    ax2.set_title(f"{subsystem} chi2 and beta-binomial chi2")
    ax2.legend()
    fig2.savefig(f"plots/chi2_{subsystem}.png", bbox_inches="tight")
except:
    pass
