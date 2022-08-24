import os

import numpy as np
import pandas as pd
import uproot

ddir = "/eos/cms/store/group/comm_dqm/DQMGUI_data/Run2018/SingleMuon/"
csvn = "goodruns-number.csv"


histlist = [
    # BMTF
    "DQMData/Run {}/L1T/Run summary/L1TStage2BMTF/bmtf_hwEta",
    "DQMData/Run {}/L1T/Run summary/L1TStage2BMTF/bmtf_hwGlobalPhi",
    "DQMData/Run {}/L1T/Run summary/L1TStage2BMTF/bmtf_hwPt",
    "DQMData/Run {}/L1T/Run summary/L1TStage2BMTF/bmtf_proc",
    # CSC
    "DQMData/Run {}/CSC/Run summary/CSCOfflineMonitor/Occupancy/hORecHits",
    "DQMData/Run {}/CSC/Run summary/CSCOfflineMonitor/Occupancy/hOStrips",
    "DQMData/Run {}/CSC/Run summary/CSCOfflineMonitor/recHits/hRHnrechits",
    "DQMData/Run {}/CSC/Run summary/CSCOfflineMonitor/Digis/hStripNFired",
    "DQMData/Run {}/CSC/Run summary/CSCOfflineMonitor/Digis/hWirenGroupsTotal",
    "DQMData/Run {}/CSC/Run summary/CSCOfflineMonitor/Segments/hSnSegments",
    "DQMData/Run {}/CSC/Run summary/CSCOfflineMonitor/Segments/hSnhits",
    "DQMData/Run {}/CSC/Run summary/CSCOfflineMonitor/Segments/hSTimeVsZ",
    # calo1
    "DQMData/Run {}/L1T/Run summary/L1TStage2CaloLayer1/ecalOccRecdEtWgt",
    "DQMData/Run {}/L1T/Run summary/L1TStage2CaloLayer1/ecalOccupancy",
    "DQMData/Run {}/L1T/Run summary/L1TStage2CaloLayer1/hcalOccRecdEtWgt",
    "DQMData/Run {}/L1T/Run summary/L1TStage2CaloLayer1/hcalOccupancy",
    # calo2
    "DQMData/Run {}/L1T/Run summary/L1TStage2CaloLayer2/Central-Jets/CenJetsPhi",
    "DQMData/Run {}/L1T/Run summary/L1TStage2CaloLayer2/Central-Jets/CenJetsEta",
    "DQMData/Run {}/L1T/Run summary/L1TStage2CaloLayer2/Forward-Jets/ForJetsEta",
    "DQMData/Run {}/L1T/Run summary/L1TStage2CaloLayer2/Forward-Jets/ForJetsPhi",
    "DQMData/Run {}/L1T/Run summary/L1TStage2CaloLayer2/Isolated-EG/IsoEGsEta",
    "DQMData/Run {}/L1T/Run summary/L1TStage2CaloLayer2/Isolated-EG/IsoEGsPhi",
    # DT
    "DQMData/Run {}/DT/Run summary/02-Segments/00-MeanRes/MeanDistr",
    "DQMData/Run {}/DT/Run summary/02-Segments/01-SigmaRes/SigmaDistr",
    "DQMData/Run {}/DT/Run summary/02-Segments/Wheel1/Sector9/Station4/T0_FromSegm_W1_Sec9_St4",
    "DQMData/Run {}/DT/Run summary/02-Segments/Wheel1/Sector9/Station4/VDrift_FromSegm_W1_Sec9_St4",
    "DQMData/Run {}/DT/Run summary/02-Segments/Wheel1/Sector9/Station4/h4DSegmNHits_W1_St4_Sec9",
    # EMTF
    "DQMData/Run {}/L1T/Run summary/L1TStage2EMTF/cscDQMOccupancy",
    "DQMData/Run {}/L1T/Run summary/L1TStage2EMTF/Timing/cscTimingTotal",
    # OMTF
    "DQMData/Run {}/L1T/Run summary/L1TStage2OMTF/omtf_hwPt",
    # RPC
    "DQMData/Run {}/RPC/Run summary/AllHits/SummaryHistograms/Occupancy_for_Endcap",
    "DQMData/Run {}/RPC/Run summary/AllHits/SummaryHistograms/Occupancy_for_Barrel",
    # uGMT
    "DQMData/Run {}/L1T/Run summary/L1TStage2uGMT/ugmtMuonBXvsLink",
    "DQMData/Run {}/L1T/Run summary/L1TStage2uGMT/ugmtMuonEta",
    "DQMData/Run {}/L1T/Run summary/L1TStage2uGMT/ugmtMuonPhi",
    "DQMData/Run {}/L1T/Run summary/L1TStage2uGMT/ugmtMuonPt",
]

runnums = pd.DataFrame(pd.read_csv(csvn)["runs"])
runnums.sort_values(by=["runs"], ignore_index=True, inplace=True)
runpath = []


eoshistdirlist = []

for x in runnums.values:
    run = x[0]
    for a, b, c in os.walk(ddir):
        if str(run)[0:4] in a:
            for fn in c:
                if (str(run) in fn) and ("UL2018" in fn):
                    eoshistdirlist.append(f"{a}/{fn}")


## pair them up???
datas = eoshistdirlist[0::10]
refs1 = eoshistdirlist[1::10]
refs2 = eoshistdirlist[3::10]
refs3 = eoshistdirlist[5::10]
refs4 = eoshistdirlist[7::10]

pairsdict = {}
for i in range(len(refs4)):
    pairsdict[datas[i]] = [refs1[i], refs2[i],refs3[i], refs4[i]]



#pairs = zip(eoshistdirlist[0::10], eoshistdirlist[5::10])
#pairsdict = {}

#for i in pairs:
#    pairsdict[i[0]] = i[1]

import json

json.dump(pairsdict, open("multirun1v1.json", "w"), indent=4)
